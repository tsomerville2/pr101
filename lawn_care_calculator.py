#!/usr/bin/env python3
"""
Lawn Care Best Window Timing Calculator

This module calculates optimal timing windows for various lawn care activities
based on seasonal patterns, temperature ranges, and regional considerations.
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, NamedTuple, Optional
import time
import threading


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


class GrassType(Enum):
    COOL_SEASON = "cool_season"
    WARM_SEASON = "warm_season"


class WeatherCondition(Enum):
    SUNNY = "sunny"
    RAINY = "rainy"
    CLOUDY = "cloudy"
    WINDY = "windy"


class TimerStatus(Enum):
    STOPPED = "stopped"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"


class SoilMoisture(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TimingWindow(NamedTuple):
    start_month: int
    end_month: int
    optimal_temp_min: int
    optimal_temp_max: int
    description: str


class WateringTimer:
    """Timer for lawn watering with countdown functionality."""
    
    def __init__(self, duration_minutes: int):
        self.original_duration = duration_minutes
        self.remaining_minutes = duration_minutes
        self.status = TimerStatus.STOPPED
        self.start_time = None
        self.pause_time = None
        self._timer_thread = None
        self._stop_event = threading.Event()
    
    def start(self):
        """Start the watering timer."""
        if self.status == TimerStatus.PAUSED:
            self.resume()
            return
            
        self.status = TimerStatus.RUNNING
        self.start_time = datetime.now()
        self._stop_event.clear()
        self._timer_thread = threading.Thread(target=self._run_timer)
        self._timer_thread.daemon = True
        self._timer_thread.start()
    
    def pause(self):
        """Pause the watering timer."""
        if self.status == TimerStatus.RUNNING:
            self.status = TimerStatus.PAUSED
            self.pause_time = datetime.now()
            self._stop_event.set()
    
    def resume(self):
        """Resume the paused watering timer."""
        if self.status == TimerStatus.PAUSED:
            # Calculate time elapsed before pause
            elapsed_before_pause = (self.pause_time - self.start_time).total_seconds() / 60
            self.remaining_minutes = max(0, self.original_duration - elapsed_before_pause)
            
            self.status = TimerStatus.RUNNING
            self.start_time = datetime.now()
            self.pause_time = None
            self._stop_event.clear()
            self._timer_thread = threading.Thread(target=self._run_timer)
            self._timer_thread.daemon = True
            self._timer_thread.start()
    
    def reset(self):
        """Reset the timer to original duration."""
        self._stop_event.set()
        self.status = TimerStatus.STOPPED
        self.remaining_minutes = self.original_duration
        self.start_time = None
        self.pause_time = None
    
    def get_status(self) -> Dict:
        """Get current timer status and remaining time."""
        if self.status == TimerStatus.RUNNING and self.start_time:
            elapsed_minutes = (datetime.now() - self.start_time).total_seconds() / 60
            current_remaining = max(0, self.remaining_minutes - elapsed_minutes)
            
            if current_remaining <= 0:
                self.status = TimerStatus.COMPLETED
                current_remaining = 0
        else:
            current_remaining = self.remaining_minutes
        
        progress_percentage = ((self.original_duration - current_remaining) / self.original_duration) * 100
        
        return {
            "status": self.status.value,
            "remaining_minutes": round(current_remaining, 1),
            "original_duration": self.original_duration,
            "progress_percentage": round(progress_percentage, 1)
        }
    
    def _run_timer(self):
        """Internal timer thread function."""
        start_remaining = self.remaining_minutes
        
        while not self._stop_event.is_set() and start_remaining > 0:
            time.sleep(1)  # Update every second
            start_remaining -= 1/60  # Subtract 1 second in minutes
            
            if start_remaining <= 0:
                self.status = TimerStatus.COMPLETED
                break
        
        if self.status == TimerStatus.RUNNING and start_remaining <= 0:
            self.status = TimerStatus.COMPLETED


class LawnCareCalculator:
    """Calculate optimal timing windows for lawn care activities."""
    
    def __init__(self, region: Region = Region.CENTRAL):
        self.region = region
        self._timing_data = self._initialize_timing_data()
        self.watering_timer = None
    
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
    
    def get_watering_frequency(self, grass_type: GrassType, season: Season = None) -> Dict:
        """Get watering frequency recommendations based on grass type and region."""
        if season is None:
            current_month = datetime.now().month
            if current_month in [3, 4, 5]:
                season = Season.SPRING
            elif current_month in [6, 7, 8]:
                season = Season.SUMMER
            elif current_month in [9, 10, 11]:
                season = Season.FALL
            else:
                season = Season.WINTER
        
        base_recommendations = {
            (GrassType.COOL_SEASON, Region.NORTHERN): {"frequency": "2-3 times", "duration": "15-20", "optimal_time": "6-8 AM"},
            (GrassType.COOL_SEASON, Region.CENTRAL): {"frequency": "2-4 times", "duration": "20-25", "optimal_time": "6-8 AM"},
            (GrassType.COOL_SEASON, Region.SOUTHERN): {"frequency": "3-4 times", "duration": "20-25", "optimal_time": "6-8 AM"},
            (GrassType.WARM_SEASON, Region.NORTHERN): {"frequency": "2-3 times", "duration": "20-25", "optimal_time": "6-8 AM"},
            (GrassType.WARM_SEASON, Region.CENTRAL): {"frequency": "3-4 times", "duration": "25-30", "optimal_time": "6-8 AM"},
            (GrassType.WARM_SEASON, Region.SOUTHERN): {"frequency": "3-4 times", "duration": "25-30", "optimal_time": "6-8 AM"}
        }
        
        recommendation = base_recommendations.get((grass_type, self.region), 
                                                {"frequency": "2-3 times", "duration": "20-25", "optimal_time": "6-8 AM"})
        
        # Adjust for season
        if season == Season.SUMMER:
            # Increase frequency in summer
            if "2-3" in recommendation["frequency"]:
                recommendation["frequency"] = "3-4 times"
            elif "3-4" in recommendation["frequency"]:
                recommendation["frequency"] = "4-5 times"
        elif season == Season.WINTER:
            # Decrease frequency in winter
            if "3-4" in recommendation["frequency"]:
                recommendation["frequency"] = "2-3 times"
            elif "4-5" in recommendation["frequency"]:
                recommendation["frequency"] = "3-4 times"
        
        recommendation["season"] = season.value
        return recommendation
    
    def create_watering_timer(self, duration_minutes: int) -> WateringTimer:
        """Create a new watering timer."""
        self.watering_timer = WateringTimer(duration_minutes)
        return self.watering_timer
    
    def get_timer_status(self) -> Optional[Dict]:
        """Get current watering timer status."""
        if self.watering_timer:
            return self.watering_timer.get_status()
        return None
    
    def calculate_next_watering(self, grass_type: GrassType, weather: WeatherCondition, 
                              temperature: float, days_since_last: int, rainfall_inches: float = 0) -> Dict:
        """Calculate when to water next based on conditions."""
        base_frequency = self.get_watering_frequency(grass_type)
        
        # Parse frequency to get max days between watering
        if "2-3" in base_frequency["frequency"]:
            max_days = 3
        elif "3-4" in base_frequency["frequency"]:
            max_days = 2
        else:
            max_days = 3
        
        # Adjust for weather conditions
        if weather == WeatherCondition.RAINY or rainfall_inches > 0.25:
            # Extend time if it rained significantly
            days_to_wait = max_days + 2
            if rainfall_inches > 0.5:
                days_to_wait += 1
            
            days_until_next = max(0, days_to_wait - days_since_last)
            advice = f"Wait {days_until_next} more days due to recent rainfall"
            
        elif weather == WeatherCondition.SUNNY and temperature > 80:
            # Water more frequently in hot, sunny conditions
            days_to_wait = max(1, max_days - 1)
            days_until_next = max(0, days_to_wait - days_since_last)
            
            if days_until_next == 0:
                advice = "Water within the next 24 hours due to hot, sunny conditions"
            else:
                advice = f"Water in {days_until_next} days - monitor for heat stress"
                
        else:
            # Normal conditions
            days_until_next = max(0, max_days - days_since_last)
            if days_until_next == 0:
                advice = "Time to water based on normal schedule"
            else:
                advice = f"Water in {days_until_next} days under normal conditions"
        
        return {
            "days_until_next_watering": days_until_next,
            "advice": advice,
            "weather_adjusted": weather != WeatherCondition.CLOUDY,
            "temperature": temperature,
            "days_since_last": days_since_last
        }
    
    def get_smart_watering_recommendation(self, grass_type: GrassType, soil_moisture: SoilMoisture,
                                        temperature: float, days_without_rain: int) -> Dict:
        """Get smart watering recommendations based on multiple factors."""
        base_frequency = self.get_watering_frequency(grass_type)
        base_duration = int(base_frequency["duration"].split("-")[1])  # Use upper range
        
        # Adjust duration based on conditions
        duration_multiplier = 1.0
        
        if soil_moisture == SoilMoisture.LOW:
            duration_multiplier += 0.25
            urgency = "immediate"
            advice = "Soil moisture is low - water immediately"
        elif soil_moisture == SoilMoisture.HIGH:
            duration_multiplier -= 0.25
            urgency = "delayed"
            advice = "Soil moisture is adequate - delay watering"
        else:
            urgency = "normal"
            advice = "Soil moisture is adequate - follow normal schedule"
        
        if temperature > 80:
            duration_multiplier += 0.1
            if urgency != "immediate":
                urgency = "soon"
            advice += " (extended duration due to heat)"
        
        if days_without_rain > 3:
            duration_multiplier += 0.15
            advice += " (dry conditions detected)"
        
        adjusted_duration = int(base_duration * duration_multiplier)
        
        return {
            "recommended_duration_minutes": adjusted_duration,
            "urgency": urgency,
            "advice": advice,
            "duration_adjustment_percentage": round((duration_multiplier - 1) * 100, 1),
            "base_duration": base_duration
        }


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