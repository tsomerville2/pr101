# Lawn Care Best Window Timing Calculator

A comprehensive tool for calculating optimal timing windows for lawn care activities based on regional climate patterns and seasonal considerations.

## Features

- **Regional Timing**: Supports Northern, Central, and Southern climate zones
- **8 Lawn Care Activities**: Seeding, Fertilizing, Dethatching, Aeration, Overseeding, Weed Control, Grub Control, Winterizing  
- **Temperature Validation**: Optimal temperature ranges for each activity
- **Next Window Calculation**: Find the next optimal timing window for any activity
- **Monthly Scheduling**: Get all optimal activities for any month
- **BDD Testing**: Comprehensive test suite with Behavior Driven Development scenarios

## Quick Start

### Basic Usage
```python
from lawn_care_calculator import LawnCareCalculator, LawnCareActivity, Region

# Create calculator for your region
calculator = LawnCareCalculator(Region.CENTRAL)

# Get timing window for seeding
window = calculator.get_timing_window(LawnCareActivity.SEEDING)
print(f"Seeding optimal: {window.start_month}-{window.end_month} months")

# Check current conditions
is_optimal = calculator.is_optimal_time(LawnCareActivity.FERTILIZING, month=5, temp=70)
print(f"May at 70°F optimal for fertilizing: {is_optimal}")
```

### Command Line Interface
```bash
# Show yearly schedule
python cli.py --schedule

# Check specific activity
python cli.py --activity seeding --region northern

# Check current conditions
python cli.py --current-optimal --month 5 --temp 70

# Get next optimal window
python cli.py --next-window overseeding
```

### Run Demo
```bash
python demo.py
```

### Run Tests
```bash
python test_lawn_care.py
```

## Activities Supported

| Activity | Description |
|----------|-------------|
| Seeding | New grass establishment |
| Fertilizing | Nutrient application |
| Dethatching | Thatch removal |
| Aeration | Soil compaction relief |
| Overseeding | Lawn density improvement |
| Weed Control | Pre/post-emergent herbicide |
| Grub Control | Insect pest management |
| Winterizing | Cold weather preparation |

## Regional Differences

The calculator accounts for climate variations across three regions:

- **Northern**: Shorter growing season, cooler temperatures
- **Central**: Moderate growing season, balanced temperatures  
- **Southern**: Extended growing season, warmer temperatures

## BDD Features

The project includes comprehensive BDD (Behavior Driven Development) scenarios in `features/lawn_care_timing.feature` that define expected behavior and validate functionality.

## Files

- `lawn_care_calculator.py` - Core calculation engine
- `cli.py` - Command-line interface
- `test_lawn_care.py` - BDD test suite
- `demo.py` - Usage demonstration
- `features/lawn_care_timing.feature` - BDD scenarios

---

*Lawn care timing calculator with regional climate considerations and optimal window calculations.*
