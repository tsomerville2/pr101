class WeatherService {
    constructor() {
        this.baseUrl = 'https://api.weather.gov';
        this.geocodingUrl = 'https://geocoding.geo.census.gov/geocoder/locations/onelineaddress';
    }

    async getCoordinatesFromLocation(location) {
        try {
            const params = new URLSearchParams({
                address: location,
                benchmark: 'Public_AR_Current',
                format: 'json'
            });
            
            const response = await fetch(`${this.geocodingUrl}?${params}`);
            const data = await response.json();
            
            if (data.result && data.result.addressMatches && data.result.addressMatches.length > 0) {
                const coords = data.result.addressMatches[0].coordinates;
                return {
                    lat: coords.y,
                    lon: coords.x,
                    address: data.result.addressMatches[0].matchedAddress
                };
            } else {
                throw new Error('Location not found');
            }
        } catch (error) {
            console.error('Geocoding error:', error);
            throw new Error('Unable to find coordinates for the specified location');
        }
    }

    async getWeatherData(lat, lon) {
        try {
            // Get grid points for the coordinates
            const pointsResponse = await fetch(`${this.baseUrl}/points/${lat},${lon}`);
            if (!pointsResponse.ok) {
                throw new Error('Failed to get weather grid information');
            }
            const pointsData = await pointsResponse.json();
            
            // Get current weather and forecast URLs
            const forecastUrl = pointsData.properties.forecast;
            const currentUrl = pointsData.properties.forecastHourly;
            
            // Fetch both current conditions and forecast
            const [forecastResponse, currentResponse] = await Promise.all([
                fetch(forecastUrl),
                fetch(currentUrl)
            ]);
            
            if (!forecastResponse.ok || !currentResponse.ok) {
                throw new Error('Failed to fetch weather data');
            }
            
            const forecastData = await forecastResponse.json();
            const currentData = await currentResponse.json();
            
            return {
                current: currentData.properties.periods[0],
                forecast: forecastData.properties.periods.slice(0, 7), // Next 7 days
                location: pointsData.properties.relativeLocation.properties
            };
        } catch (error) {
            console.error('Weather API error:', error);
            throw new Error('Unable to fetch weather data from the National Weather Service');
        }
    }

    formatTemperature(temp, unit) {
        return `${temp}°${unit}`;
    }

    formatTime(timeString) {
        const date = new Date(timeString);
        return date.toLocaleString();
    }
}

class WeatherUI {
    constructor() {
        this.weatherService = new WeatherService();
        this.displayElement = document.getElementById('weatherDisplay');
    }

    showLoading() {
        this.displayElement.innerHTML = '<div class="loading">Loading weather data...</div>';
    }

    showError(message) {
        this.displayElement.innerHTML = `<div class="error">Error: ${message}</div>`;
    }

    displayWeather(weatherData, coordinates, address) {
        let html = `
            <div class="weather-card current-weather">
                <div class="weather-title">Current Conditions</div>
                <div class="weather-detail"><strong>Location:</strong> ${address}</div>
                <div class="weather-detail"><strong>Temperature:</strong> ${this.weatherService.formatTemperature(weatherData.current.temperature, weatherData.current.temperatureUnit)}</div>
                <div class="weather-detail"><strong>Conditions:</strong> ${weatherData.current.shortForecast}</div>
                <div class="weather-detail"><strong>Wind:</strong> ${weatherData.current.windDirection} ${weatherData.current.windSpeed}</div>
                <div class="weather-detail"><strong>Time:</strong> ${this.weatherService.formatTime(weatherData.current.startTime)}</div>
                <div class="coordinates">Coordinates: ${coordinates.lat.toFixed(4)}, ${coordinates.lon.toFixed(4)}</div>
            </div>
        `;

        html += '<div class="weather-title" style="margin-top: 20px; margin-bottom: 15px;">7-Day Forecast</div>';
        
        weatherData.forecast.forEach(period => {
            html += `
                <div class="weather-card forecast-item">
                    <div class="weather-detail"><strong>${period.name}:</strong></div>
                    <div class="weather-detail">Temperature: ${this.weatherService.formatTemperature(period.temperature, period.temperatureUnit)}</div>
                    <div class="weather-detail">Conditions: ${period.shortForecast}</div>
                    <div class="weather-detail">Wind: ${period.windDirection} ${period.windSpeed}</div>
                    ${period.detailedForecast ? `<div class="weather-detail">Details: ${period.detailedForecast}</div>` : ''}
                </div>
            `;
        });

        this.displayElement.innerHTML = html;
    }

    async fetchAndDisplayWeather(location) {
        if (!location.trim()) {
            this.showError('Please enter a location');
            return;
        }

        this.showLoading();
        
        try {
            // Get coordinates from location
            const coordinates = await this.weatherService.getCoordinatesFromLocation(location);
            
            // Get weather data
            const weatherData = await this.weatherService.getWeatherData(coordinates.lat, coordinates.lon);
            
            // Display the results
            this.displayWeather(weatherData, coordinates, coordinates.address);
            
        } catch (error) {
            this.showError(error.message);
        }
    }
}

// Initialize the weather UI
const weatherUI = new WeatherUI();

// Main function called by the button
async function getWeatherData() {
    const location = document.getElementById('locationInput').value;
    const button = document.querySelector('button');
    
    // Disable button during request
    button.disabled = true;
    button.textContent = 'Loading...';
    
    try {
        await weatherUI.fetchAndDisplayWeather(location);
    } finally {
        // Re-enable button
        button.disabled = false;
        button.textContent = 'Get Weather';
    }
}

// Allow Enter key to trigger search
document.getElementById('locationInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        getWeatherData();
    }
});

// Example usage on page load
document.addEventListener('DOMContentLoaded', function() {
    // You can set a default location here if desired
    // document.getElementById('locationInput').value = 'Washington, DC';
});