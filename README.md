# Weather Data Dashboard

A simple web application that gathers weather data from the National Weather Service (NWS) API and displays it in an HTML user interface.

## Features

- **Government Data Source**: Uses the free National Weather Service API (weather.gov)
- **Current Conditions**: Displays current temperature, conditions, and wind information
- **7-Day Forecast**: Shows detailed weather forecast for the next week
- **Location Search**: Enter any US city and state to get weather data
- **Responsive Design**: Clean, mobile-friendly interface

## Usage

1. Open `index.html` in a web browser
2. Enter a location in the format "City, State" (e.g., "Denver, CO")
3. Click "Get Weather" or press Enter
4. View current conditions and 7-day forecast

## Technical Details

### APIs Used
- **National Weather Service API** (api.weather.gov) - Free government weather data
- **US Census Geocoding API** - Convert addresses to coordinates

### Files
- `index.html` - Main HTML interface with styling
- `weather.js` - JavaScript application logic and API integration

### Data Flow
1. User enters location → Geocoding API converts to coordinates
2. Coordinates → NWS API provides weather grid information
3. Grid data → Fetch current conditions and forecast
4. Display formatted weather information in the UI

## Example Usage

```
Location: "Seattle, WA"
→ Current: 65°F, Partly Cloudy, Wind: W 10 mph
→ Forecast: 7-day detailed weather outlook
```

## Browser Compatibility

Works in modern browsers that support:
- ES6+ JavaScript features (classes, async/await)
- Fetch API
- CSS Grid/Flexbox

## Note

This application uses CORS-enabled government APIs. No server setup required - runs entirely in the browser.