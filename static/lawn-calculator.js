class LawnCalculator {
    constructor() {
        this.map = null;
        this.drawnItems = null;
        this.drawControl = null;
        this.currentPolygon = null;
        this.area = 0;

        this.init();
    }

    init() {
        this.initMap();
        this.setupEventListeners();
        this.updateSchedule();
    }

    initMap() {
        // Initialize map centered on US
        this.map = L.map('map').setView([39.8283, -98.5795], 4);

        // Add OpenStreetMap tile layer
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(this.map);

        // Initialize drawn items layer
        this.drawnItems = new L.FeatureGroup();
        this.map.addLayer(this.drawnItems);

        // Initialize drawing controls
        this.drawControl = new L.Control.Draw({
            position: 'topright',
            draw: {
                rectangle: false,
                circle: false,
                circlemarker: false,
                marker: false,
                polyline: false,
                polygon: {
                    allowIntersection: false,
                    drawError: {
                        color: '#e1e100',
                        message: '<strong>Error:</strong> Shape edges cannot cross!'
                    },
                    shapeOptions: {
                        color: '#4CAF50',
                        weight: 3,
                        fillOpacity: 0.3
                    }
                }
            },
            edit: {
                featureGroup: this.drawnItems,
                remove: true
            }
        });

        // Add drawing controls to map
        this.map.addControl(this.drawControl);

        // Handle drawing events
        this.map.on('draw:created', (e) => this.onDrawCreated(e));
        this.map.on('draw:deleted', () => this.onDrawDeleted());
        this.map.on('draw:edited', (e) => this.onDrawEdited(e));
    }

    setupEventListeners() {
        // Search functionality
        document.getElementById('search-btn').addEventListener('click', () => this.searchLocation());
        document.getElementById('search-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.searchLocation();
        });

        // Drawing controls
        document.getElementById('draw-btn').addEventListener('click', () => this.toggleDrawing());
        document.getElementById('clear-btn').addEventListener('click', () => this.clearDrawing());
        document.getElementById('calculate-btn').addEventListener('click', () => this.calculateArea());

        // Region selection
        document.getElementById('region-select').addEventListener('change', () => this.updateSchedule());
    }

    async searchLocation() {
        const query = document.getElementById('search-input').value.trim();
        const status = document.getElementById('search-status');

        if (!query) {
            status.textContent = 'Please enter a location to search';
            status.className = 'error';
            return;
        }

        status.textContent = 'Searching...';
        status.className = 'loading';

        try {
            // Using Nominatim API for geocoding
            const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=1`);
            const data = await response.json();

            if (data.length > 0) {
                const lat = parseFloat(data[0].lat);
                const lon = parseFloat(data[0].lon);
                
                this.map.setView([lat, lon], 18);
                
                // Add a temporary marker
                const marker = L.marker([lat, lon]).addTo(this.map)
                    .bindPopup(`<b>${data[0].display_name}</b><br>Zoom in and draw your lawn area`)
                    .openPopup();

                // Remove marker after 5 seconds
                setTimeout(() => this.map.removeLayer(marker), 5000);

                status.textContent = `Found: ${data[0].display_name}`;
                status.className = 'success';
            } else {
                status.textContent = 'Location not found. Try a different search term.';
                status.className = 'error';
            }
        } catch (error) {
            console.error('Search error:', error);
            status.textContent = 'Search failed. Please try again.';
            status.className = 'error';
        }
    }

    toggleDrawing() {
        const drawBtn = document.getElementById('draw-btn');
        
        if (this.drawControl._toolbars.draw._modes.polygon.handler.enabled()) {
            this.drawControl._toolbars.draw._modes.polygon.handler.disable();
            drawBtn.textContent = '🖊️ Draw Area';
            drawBtn.classList.remove('active');
        } else {
            this.drawControl._toolbars.draw._modes.polygon.handler.enable();
            drawBtn.textContent = '⏹️ Stop Drawing';
            drawBtn.classList.add('active');
        }
    }

    clearDrawing() {
        this.drawnItems.clearLayers();
        this.currentPolygon = null;
        this.area = 0;
        this.updateResults();
        document.getElementById('calculate-btn').disabled = true;
    }

    onDrawCreated(e) {
        const layer = e.layer;
        
        // Remove existing polygon if any
        if (this.currentPolygon) {
            this.drawnItems.removeLayer(this.currentPolygon);
        }
        
        this.currentPolygon = layer;
        this.drawnItems.addLayer(layer);
        
        document.getElementById('calculate-btn').disabled = false;
        document.getElementById('draw-btn').textContent = '🖊️ Draw Area';
        document.getElementById('draw-btn').classList.remove('active');
    }

    onDrawDeleted() {
        this.currentPolygon = null;
        this.area = 0;
        this.updateResults();
        document.getElementById('calculate-btn').disabled = true;
    }

    onDrawEdited(e) {
        if (this.currentPolygon) {
            document.getElementById('calculate-btn').disabled = false;
        }
    }

    calculateArea() {
        if (!this.currentPolygon) return;

        // Calculate area using Leaflet's built-in method
        // This gives us area in square meters
        const areaM2 = L.GeometryUtil.geodesicArea(this.currentPolygon.getLatLngs()[0]);
        
        // Convert to square feet (1 m² = 10.764 ft²)
        this.area = areaM2 * 10.764;
        
        this.updateResults();
        this.calculateCosts();
    }

    updateResults() {
        const areaElement = document.querySelector('#area-result .value');
        const acresElement = document.getElementById('area-acres');
        
        areaElement.textContent = Math.round(this.area).toLocaleString();
        acresElement.textContent = (this.area / 43560).toFixed(3);
    }

    calculateCosts() {
        if (this.area === 0) {
            this.clearCosts();
            return;
        }

        // Cost calculation based on typical lawn care prices
        // These are estimates - in a real app, these might come from an API or database
        const costs = {
            seeding: this.area * 0.15,        // $0.15 per sq ft
            fertilizer: this.area * 0.05,     // $0.05 per sq ft
            service: this.area * 0.25         // $0.25 per sq ft for professional service
        };

        costs.total = costs.seeding + costs.fertilizer + costs.service;

        // Update UI
        document.getElementById('seeding-cost').textContent = `$${costs.seeding.toFixed(2)}`;
        document.getElementById('fertilizer-cost').textContent = `$${costs.fertilizer.toFixed(2)}`;
        document.getElementById('service-cost').textContent = `$${costs.service.toFixed(2)}`;
        document.getElementById('total-cost').textContent = `$${costs.total.toFixed(2)}`;
    }

    clearCosts() {
        document.getElementById('seeding-cost').textContent = '$0';
        document.getElementById('fertilizer-cost').textContent = '$0';
        document.getElementById('service-cost').textContent = '$0';
        document.getElementById('total-cost').textContent = '$0';
    }

    updateSchedule() {
        const region = document.getElementById('region-select').value;
        const activitiesDiv = document.getElementById('current-activities');
        
        // Get current month (1-12)
        const currentMonth = new Date().getMonth() + 1;
        
        // This would typically call your Python backend
        // For now, we'll use simplified logic based on the existing calculator
        const activities = this.getCurrentActivities(region, currentMonth);
        
        if (activities.length > 0) {
            activitiesDiv.innerHTML = `
                <h4>Recommended for ${this.getMonthName(currentMonth)}:</h4>
                <ul>
                    ${activities.map(activity => `<li>${activity}</li>`).join('')}
                </ul>
            `;
        } else {
            activitiesDiv.innerHTML = '<p>No specific activities recommended for this month.</p>';
        }
    }

    getCurrentActivities(region, month) {
        // Simplified activity scheduling based on the Python calculator logic
        const schedules = {
            northern: {
                1: [], 2: [], 3: ['Dethatching'], 4: ['Seeding', 'Fertilizing', 'Dethatching', 'Aeration'],
                5: ['Seeding', 'Fertilizing', 'Dethatching', 'Aeration', 'Grub Control'], 6: ['Fertilizing', 'Grub Control'],
                7: ['Fertilizing', 'Weed Control', 'Grub Control'], 8: ['Fertilizing', 'Weed Control', 'Overseeding', 'Grub Control'],
                9: ['Fertilizing', 'Weed Control', 'Overseeding'], 10: ['Fertilizing', 'Winterizing'],
                11: ['Winterizing'], 12: []
            },
            central: {
                1: [], 2: [], 3: ['Fertilizing', 'Dethatching'], 4: ['Seeding', 'Fertilizing', 'Dethatching', 'Aeration'],
                5: ['Seeding', 'Fertilizing', 'Dethatching', 'Aeration', 'Grub Control'], 6: ['Seeding', 'Fertilizing', 'Aeration', 'Grub Control'],
                7: ['Fertilizing', 'Weed Control', 'Aeration', 'Grub Control'], 8: ['Fertilizing', 'Weed Control', 'Overseeding', 'Grub Control'],
                9: ['Fertilizing', 'Weed Control', 'Overseeding', 'Grub Control'], 10: ['Fertilizing', 'Weed Control', 'Overseeding'],
                11: ['Fertilizing', 'Overseeding', 'Winterizing'], 12: ['Winterizing']
            },
            southern: {
                1: ['Fertilizing', 'Weed Control'], 2: ['Fertilizing', 'Dethatching', 'Weed Control'], 3: ['Seeding', 'Fertilizing', 'Dethatching', 'Weed Control'],
                4: ['Seeding', 'Fertilizing', 'Dethatching', 'Weed Control'], 5: ['Seeding', 'Fertilizing', 'Aeration', 'Weed Control', 'Grub Control'],
                6: ['Fertilizing', 'Aeration', 'Weed Control', 'Grub Control'], 7: ['Fertilizing', 'Aeration', 'Weed Control', 'Grub Control'],
                8: ['Fertilizing', 'Weed Control', 'Grub Control'], 9: ['Fertilizing', 'Weed Control', 'Overseeding', 'Grub Control'],
                10: ['Fertilizing', 'Weed Control', 'Overseeding', 'Grub Control'], 11: ['Fertilizing', 'Weed Control', 'Overseeding'],
                12: ['Winterizing']
            }
        };

        return schedules[region][month] || [];
    }

    getMonthName(month) {
        const months = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December'];
        return months[month];
    }
}

// Initialize the calculator when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new LawnCalculator();
});

// Add Leaflet geometry utilities if not available
if (!L.GeometryUtil) {
    L.GeometryUtil = {
        // Calculate geodesic area of a polygon
        geodesicArea: function(latLngs) {
            let area = 0;
            const len = latLngs.length;
            
            if (len < 3) return 0;
            
            for (let i = 0; i < len; i++) {
                const j = (i + 1) % len;
                const xi = latLngs[i].lng * Math.PI / 180;
                const yi = latLngs[i].lat * Math.PI / 180;
                const xj = latLngs[j].lng * Math.PI / 180;
                const yj = latLngs[j].lat * Math.PI / 180;
                
                area += (xj - xi) * (2 + Math.sin(yi) + Math.sin(yj));
            }
            
            area = Math.abs(area * 6378137 * 6378137 / 2);
            return area;
        }
    };
}