# Domain Model - Lawn Care Timing Calculator

## Bounded Context
Lawn Care Scheduling - A focused context for calculating and managing optimal timing windows for lawn care activities based on seasonal patterns, regional climate differences, and temperature requirements.

## Aggregates

### LawnCareSchedule
- **Root Entity**: TimingWindow
- **Value Objects**: 
  - Region (Northern, Central, Southern)
  - LawnCareActivity (Seeding, Fertilizing, Dethatching, etc.)
  - TemperatureRange (min/max optimal temperatures)
  - MonthRange (start/end months for optimal timing)
- **Business Rules**: 
  - Each activity has specific optimal temperature ranges
  - Regional climate differences affect timing by 2-4 weeks
  - Activities cannot be scheduled outside their seasonal windows

### ActivitySchedule
- **Root Entity**: ScheduledActivity
- **Value Objects**:
  - ActivityStatus (Optimal, Suboptimal, NotRecommended)
  - Season (Spring, Summer, Fall, Winter)
- **Business Rules**:
  - Temperature must be within optimal range for recommendation
  - Regional adjustments applied automatically
  - Next optimal window calculated based on current date

## Domain Events
- TimingWindowCalculated - When optimal timing window is determined for an activity
- RegionalAdjustmentApplied - When timing is adjusted based on climate zone
- OptimalConditionsDetected - When current conditions match activity requirements
- ScheduleGenerated - When yearly schedule is created for a region

## Ubiquitous Language
- **Timing Window**: The optimal date range for performing a lawn care activity
- **Regional Zone**: Geographic climate classification (Northern/Central/Southern)
- **Activity**: Specific lawn care task with defined requirements
- **Optimal Conditions**: Temperature and seasonal requirements met
- **Seasonal Adjustment**: Timing modification based on regional climate
- **Temperature Range**: Min/max temperatures for optimal activity performance
- **Next Window**: Earliest future date when conditions will be optimal
- **Growing Season**: Period when grass actively grows (varies by region)