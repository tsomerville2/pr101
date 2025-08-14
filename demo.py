#!/usr/bin/env python3
"""
Demo script showing Lawn Care Calculator functionality
"""

from lawn_care_calculator import LawnCareCalculator, LawnCareActivity, Region
from datetime import datetime


def demo_basic_functionality():
    """Demonstrate basic calculator functionality"""
    print("🌱 Lawn Care Best Window Timing Calculator Demo")
    print("=" * 55)
    
    # Create calculator for central region
    calculator = LawnCareCalculator(Region.CENTRAL)
    
    print(f"\nCalculator initialized for {calculator.region.value.title()} region")
    
    # Show seeding window example
    print("\n📌 Example: Seeding Timing")
    print("-" * 25)
    window = calculator.get_timing_window(LawnCareActivity.SEEDING)
    print(f"Optimal months: {window.start_month} to {window.end_month}")
    print(f"Temperature range: {window.optimal_temp_min}°F - {window.optimal_temp_max}°F")
    print(f"Description: {window.description}")
    
    # Check if May 70°F is good for fertilizing
    print("\n📌 Example: Current Conditions Check")
    print("-" * 35)
    is_optimal = calculator.is_optimal_time(LawnCareActivity.FERTILIZING, 5, 70)
    print(f"Is May at 70°F optimal for fertilizing? {'✅ Yes' if is_optimal else '❌ No'}")
    
    # Show next window for overseeding
    print("\n📌 Example: Next Optimal Window")
    print("-" * 30)
    next_window = calculator.get_next_optimal_window(LawnCareActivity.OVERSEEDING)
    print(f"Next overseeding window: {next_window['start_date']} to {next_window['end_date']}")
    print(f"Days until start: {next_window['days_until_start']}")
    
    # Show activities for April
    print("\n📌 Example: Monthly Activities")
    print("-" * 28)
    april_activities = calculator.get_all_activities_for_month(4)
    print("April activities:")
    for activity in april_activities:
        print(f"  • {activity.value.replace('_', ' ').title()}")


def demo_regional_differences():
    """Show how regions affect timing"""
    print("\n🌍 Regional Timing Differences")
    print("=" * 32)
    
    regions = [Region.NORTHERN, Region.CENTRAL, Region.SOUTHERN]
    
    for region in regions:
        calc = LawnCareCalculator(region)
        window = calc.get_timing_window(LawnCareActivity.SEEDING)
        print(f"\n{region.value.title()} Region:")
        print(f"  Seeding: Months {window.start_month}-{window.end_month}")
        print(f"  Temp: {window.optimal_temp_min}°F-{window.optimal_temp_max}°F")


def demo_yearly_schedule():
    """Show a condensed yearly schedule"""
    print("\n📅 Yearly Schedule Overview")
    print("=" * 28)
    
    calculator = LawnCareCalculator(Region.CENTRAL)
    schedule = calculator.get_monthly_schedule()
    
    month_names = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    for month, activities in schedule.items():
        activity_count = len(activities)
        print(f"{month_names[month]:>3}: {activity_count} activities - {', '.join(activities[:2])}{' ...' if activity_count > 2 else ''}")


def demo_bdd_scenarios():
    """Demo key BDD scenarios"""
    print("\n🧪 BDD Scenario Validation")
    print("=" * 27)
    
    calculator = LawnCareCalculator(Region.CENTRAL)
    
    # Test scenario: Seeding window validation
    window = calculator.get_timing_window(LawnCareActivity.SEEDING)
    scenario_1_pass = (window.start_month == 4 and window.end_month == 6 
                      and window.optimal_temp_min == 55 and window.optimal_temp_max == 80)
    print(f"✅ Seeding window scenario: {'PASS' if scenario_1_pass else 'FAIL'}")
    
    # Test scenario: Optimal conditions
    scenario_2_pass = calculator.is_optimal_time(LawnCareActivity.FERTILIZING, 5, 70)
    print(f"✅ Optimal fertilizing conditions: {'PASS' if scenario_2_pass else 'FAIL'}")
    
    # Test scenario: Non-optimal conditions  
    scenario_3_pass = not calculator.is_optimal_time(LawnCareActivity.WINTERIZING, 6, 85)
    print(f"✅ Non-optimal winterizing conditions: {'PASS' if scenario_3_pass else 'FAIL'}")
    
    # Test scenario: Spring activities
    spring_activities = calculator.get_all_activities_for_month(4)
    spring_values = [activity.value for activity in spring_activities]
    scenario_4_pass = all(activity in spring_values for activity in ['seeding', 'fertilizing', 'dethatching', 'aeration'])
    print(f"✅ Spring peak activities: {'PASS' if scenario_4_pass else 'FAIL'}")


if __name__ == "__main__":
    demo_basic_functionality()
    demo_regional_differences() 
    demo_yearly_schedule()
    demo_bdd_scenarios()
    
    print("\n" + "=" * 55)
    print("🎉 Demo Complete!")
    print("\nUsage Examples:")
    print("  python cli.py --schedule")
    print("  python cli.py --activity seeding --region northern") 
    print("  python cli.py --current-optimal --month 5 --temp 70")
    print("  python cli.py --next-window overseeding")