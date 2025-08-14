#!/usr/bin/env python3
"""
Lawn Care Best Window Timing Calculator

This module calculates optimal timing windows for various lawn care activities
based on seasonal patterns, temperature ranges, and regional considerations.
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, NamedTuple, Optional


class Season(Enum):
    SPRING = "spring"
    SUMMER = "summer"
    FALL = "fall" 
    WINTER = "winter"


class Region(Enum):
    NORTHERN = "northern"
    CENTRAL = "central"
    SOUTHERN = "southern"


class LawnCareActivity(Enum):
    SEEDING = "seeding"
    FERTILIZING = "fertilizing"
    DETHATCHING = "dethatching"
    AERATION = "aeration"
    OVERSEEDING = "overseeding"
    WEED_CONTROL = "weed_control"
    GRUB_CONTROL = "grub_control"
    WINTERIZING = "winterizing"


class TimingWindow(NamedTuple):
    start_month: int
    end_month: int
    optimal_temp_min: int
    optimal_temp_max: int
    description: str


class LawnCareCalculator:
    """Calculate optimal timing windows for lawn care activities."""
    
    def __init__(self, region: Region = Region.CENTRAL):
        self.region = region
        self._timing_data = self._initialize_timing_data()
    
    def _initialize_timing_data(self) -> Dict[LawnCareActivity, Dict[Region, TimingWindow]]:
        """Initialize timing data for different activities and regions."""
        return {
            LawnCareActivity.SEEDING: {
                Region.NORTHERN: TimingWindow(4, 5, 50, 75, "Cool season grass seeding in spring"),
                Region.CENTRAL: TimingWindow(4, 6, 55, 80, "Spring seeding window"),
                Region.SOUTHERN: TimingWindow(3, 5, 60, 85, "Early spring seeding for warm season")
            },
            LawnCareActivity.FERTILIZING: {
                Region.NORTHERN: TimingWindow(4, 10, 45, 85, "Growing season fertilization"),
                Region.CENTRAL: TimingWindow(3, 11, 50, 90, "Extended growing season"),
                Region.SOUTHERN: TimingWindow(2, 11, 55, 95, "Year-round growing potential")
            },
            LawnCareActivity.DETHATCHING: {
                Region.NORTHERN: TimingWindow(4, 5, 50, 70, "Spring dethatching when soil workable"),
                Region.CENTRAL: TimingWindow(3, 5, 45, 75, "Early spring dethatching"),
                Region.SOUTHERN: TimingWindow(2, 4, 50, 80, "Late winter to early spring")
            },
            LawnCareActivity.AERATION: {
                Region.NORTHERN: TimingWindow(4, 5, 45, 75, "Spring aeration for cool season"),
                Region.CENTRAL: TimingWindow(4, 6, 50, 80, "Spring to early summer"),
                Region.SOUTHERN: TimingWindow(5, 7, 60, 90, "Late spring to early summer")
            },
            LawnCareActivity.OVERSEEDING: {
                Region.NORTHERN: TimingWindow(8, 9, 60, 75, "Fall overseeding optimal"),
                Region.CENTRAL: TimingWindow(8, 10, 55, 80, "Extended fall window"),
                Region.SOUTHERN: TimingWindow(9, 11, 60, 85, "Fall into early winter")
            },
            LawnCareActivity.WEED_CONTROL: {
                Region.NORTHERN: TimingWindow(4, 9, 50, 85, "Pre and post-emergent timing"),
                Region.CENTRAL: TimingWindow(3, 10, 45, 90, "Extended weed control season"),
                Region.SOUTHERN: TimingWindow(2, 11, 50, 95, "Nearly year-round control needed")
            },
            LawnCareActivity.GRUB_CONTROL: {
                Region.NORTHERN: TimingWindow(7, 8, 70, 85, "Summer grub control"),
                Region.CENTRAL: TimingWindow(6, 9, 65, 90, "Extended grub season"),
                Region.SOUTHERN: TimingWindow(5, 10, 70, 95, "Long grub control period")
            },
            LawnCareActivity.WINTERIZING: {
                Region.NORTHERN: TimingWindow(10, 11, 35, 55, "Prepare for harsh winter"),
                Region.CENTRAL: TimingWindow(11, 12, 40, 60, "Mid to late fall preparation"),
                Region.SOUTHERN: TimingWindow(12, 1, 45, 65, "Minimal winterization needed")
            }
        }
    
    def get_timing_window(self, activity: LawnCareActivity) -> TimingWindow:
        """Get the timing window for a specific activity in the current region."""
        return self._timing_data[activity][self.region]
    
    def is_optimal_time(self, activity: LawnCareActivity, current_month: int, current_temp: int) -> bool:
        """Check if current conditions are optimal for the given activity."""
        window = self.get_timing_window(activity)
        
        # Handle winter months that span year boundary
        if window.start_month > window.end_month:
            month_ok = current_month >= window.start_month or current_month <= window.end_month
        else:
            month_ok = window.start_month <= current_month <= window.end_month
            
        temp_ok = window.optimal_temp_min <= current_temp <= window.optimal_temp_max
        
        return month_ok and temp_ok
    
    def get_next_optimal_window(self, activity: LawnCareActivity, from_date: Optional[datetime] = None) -> Dict:
        """Calculate the next optimal window for an activity."""
        if from_date is None:
            from_date = datetime.now()
            
        window = self.get_timing_window(activity)
        current_year = from_date.year
        
        # Calculate start date for this year
        start_date = datetime(current_year, window.start_month, 1)
        
        # If we've passed this year's window, calculate for next year
        if from_date > start_date:
            if window.start_month > window.end_month:  # Spans year boundary
                if from_date.month <= window.end_month:
                    # We're in the current window
                    end_date = datetime(current_year, window.end_month, 28)
                else:
                    # Next window starts later this year
                    start_date = datetime(current_year, window.start_month, 1)
                    end_date = datetime(current_year + 1, window.end_month, 28)
            else:
                # Next year's window
                start_date = datetime(current_year + 1, window.start_month, 1)
                end_date = datetime(current_year + 1, window.end_month, 28)
        else:
            # This year's window
            if window.start_month > window.end_month:
                end_date = datetime(current_year + 1, window.end_month, 28)
            else:
                end_date = datetime(current_year, window.end_month, 28)
        
        days_until = (start_date - from_date).days
        window_length = (end_date - start_date).days
        
        return {
            "activity": activity.value,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "days_until_start": max(0, days_until),
            "window_length_days": window_length,
            "optimal_temp_range": f"{window.optimal_temp_min}°F - {window.optimal_temp_max}°F",
            "description": window.description
        }
    
    def get_all_activities_for_month(self, month: int) -> List[LawnCareActivity]:
        """Get all activities that are optimal for a given month."""
        optimal_activities = []
        
        for activity in LawnCareActivity:
            window = self.get_timing_window(activity)
            
            # Handle winter months that span year boundary
            if window.start_month > window.end_month:
                if month >= window.start_month or month <= window.end_month:
                    optimal_activities.append(activity)
            else:
                if window.start_month <= month <= window.end_month:
                    optimal_activities.append(activity)
                    
        return optimal_activities
    
    def get_monthly_schedule(self) -> Dict[int, List[str]]:
        """Generate a yearly schedule of lawn care activities by month."""
        schedule = {}
        
        for month in range(1, 13):
            activities = self.get_all_activities_for_month(month)
            schedule[month] = [activity.value for activity in activities]
            
        return schedule


def main():
    """Demo the lawn care calculator functionality."""
    calculator = LawnCareCalculator(Region.CENTRAL)
    
    print("Lawn Care Best Window Timing Calculator")
    print("=" * 50)
    
    # Show next optimal windows for all activities
    print("\nNext Optimal Windows for All Activities:")
    print("-" * 40)
    
    for activity in LawnCareActivity:
        window_info = calculator.get_next_optimal_window(activity)
        print(f"\n{activity.value.replace('_', ' ').title()}:")
        print(f"  Window: {window_info['start_date']} to {window_info['end_date']}")
        print(f"  Days until start: {window_info['days_until_start']}")
        print(f"  Optimal temperature: {window_info['optimal_temp_range']}")
        print(f"  Notes: {window_info['description']}")
    
    # Show monthly schedule
    print("\n\nMonthly Activity Schedule:")
    print("-" * 30)
    month_names = ["", "January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]
    
    schedule = calculator.get_monthly_schedule()
    for month, activities in schedule.items():
        if activities:
            print(f"\n{month_names[month]}:")
            for activity in activities:
                print(f"  - {activity.replace('_', ' ').title()}")


if __name__ == "__main__":
    main()