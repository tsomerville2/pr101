# Lawn Care Calculator

A comprehensive lawn care timing calculator with an interactive map-based UI for calculating lawn area and estimating costs.

## Features

### 🌱 Lawn Care Timing Calculator
- **Regional optimization**: Supports Northern, Central, and Southern regions
- **Seasonal timing**: Calculates optimal windows for various lawn care activities
- **Activity tracking**: Covers seeding, fertilizing, dethatching, aeration, overseeding, weed control, grub control, and winterizing
- **Temperature-based recommendations**: Considers optimal temperature ranges

### 🗺️ Interactive Map Interface
- **Location search**: Find your property using address search
- **Visual lawn selection**: Draw your lawn area directly on the map
- **Area calculation**: Automatically calculates square footage and acreage
- **Cost estimation**: Provides cost estimates for different lawn care services

## Components

### Core Calculator (`lawn_care_calculator.py`)
The main calculation engine that provides:
- Timing windows for different activities by region
- Temperature-based optimization
- Next optimal window calculations
- Monthly activity scheduling

### Command Line Interface (`cli.py`)
Full-featured CLI for:
- Activity-specific timing queries
- Current condition optimization checks
- Yearly schedule generation
- Regional customization

### Web Interface (`web_server.py` + `static/`)
Interactive web application featuring:
- **Map Integration**: Leaflet.js with OpenStreetMap tiles
- **Drawing Tools**: Polygon drawing for lawn area selection  
- **Real-time Calculations**: Instant area and cost calculations
- **Responsive Design**: Works on desktop and mobile devices
- **API Endpoints**: RESTful API for schedule and timing data

## Usage

### Command Line
```bash
# Show yearly schedule for central region
python cli.py --schedule --region central

# Check specific activity timing
python cli.py --activity seeding --region northern

# Check current optimal conditions
python cli.py --current-optimal --month 5 --temp 70 --region central

# Show next window for specific activity
python cli.py --next-window fertilizing
```

### Web Interface
```bash
# Start the web server
python web_server.py --port 8000

# Access the interface
# Open http://localhost:8000 in your browser
```

#### Using the Web Interface:
1. **Search Location**: Enter your address to find your property
2. **Draw Lawn Area**: Use the drawing tool to outline your lawn
3. **Calculate**: Get instant area measurements and cost estimates
4. **View Schedule**: See recommended activities for your region and current month

## API Endpoints

- `GET /api/schedule?region=central&month=8` - Get activities for specific region/month
- `GET /api/timing?activity=seeding&region=northern` - Get timing window for specific activity

## Cost Calculations

The web interface provides cost estimates based on typical market rates:
- **Seeding**: $0.15 per square foot
- **Fertilizer**: $0.05 per square foot  
- **Professional Service**: $0.25 per square foot

*Note: Prices are estimates and may vary by location and service provider.*

## Technology Stack

- **Backend**: Python 3.7+ with built-in HTTP server
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Mapping**: Leaflet.js with OpenStreetMap
- **Drawing**: Leaflet Draw plugin
- **Geocoding**: Nominatim API
- **Testing**: Behave (BDD framework)

## Installation

No additional dependencies required! Uses Python standard library and CDN-hosted frontend libraries.

```bash
# Clone the repository
git clone <repository-url>

# Run the web server
python web_server.py

# Or use the CLI
python cli.py --help
```

## Browser Compatibility

- Modern browsers with JavaScript enabled
- Mobile responsive design
- Requires internet connection for map tiles and geocoding