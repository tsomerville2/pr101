#!/usr/bin/env python3
"""
Command-line interface for the Lawn Care Calculator
"""

import argparse
import sys
from datetime import datetime
from lawn_care_calculator import LawnCareCalculator, LawnCareActivity, Region
from crab_grass_knowledge_base import CrabGrassKnowledgeBase, CrabGrassType, CrabGrassStage


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Lawn Care Best Window Timing Calculator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py --activity seeding --region northern
  python cli.py --schedule
  python cli.py --current-optimal --month 5 --temp 70
  python cli.py --next-window fertilizing
        """
    )
    
    parser.add_argument('--region', '-r', 
                       choices=['northern', 'central', 'southern'],
                       default='central',
                       help='Geographic region (default: central)')
    
    parser.add_argument('--activity', '-a',
                       choices=[activity.value for activity in LawnCareActivity],
                       help='Specific lawn care activity to check')
    
    parser.add_argument('--schedule', '-s',
                       action='store_true',
                       help='Show full yearly schedule')
    
    parser.add_argument('--current-optimal', '-c',
                       action='store_true',
                       help='Check if current conditions are optimal (requires --month and --temp)')
    
    parser.add_argument('--month', '-m',
                       type=int,
                       choices=range(1, 13),
                       help='Month number (1-12)')
    
    parser.add_argument('--temp', '-t',
                       type=int,
                       help='Temperature in Fahrenheit')
    
    parser.add_argument('--next-window', '-n',
                       choices=[activity.value for activity in LawnCareActivity],
                       help='Show next optimal window for activity')
    
    # Crab grass knowledge base options
    parser.add_argument('--crabgrass', '-cg',
                       action='store_true',
                       help='Access crab grass knowledge base')
    
    parser.add_argument('--identify', '-id',
                       nargs='+',
                       help='Identify crab grass type based on observed features')
    
    parser.add_argument('--treatment', '-tr',
                       action='store_true',
                       help='Get crab grass treatment recommendations')
    
    parser.add_argument('--prevention', '-pr',
                       action='store_true',
                       help='Show crab grass prevention strategies')
    
    parser.add_argument('--lifecycle', '-lc',
                       action='store_true',
                       help='Show crab grass lifecycle information')
    
    parser.add_argument('--calendar', '-cal',
                       action='store_true',
                       help='Show seasonal crab grass management calendar')
    
    args = parser.parse_args()
    
    # Initialize calculator
    region = Region(args.region)
    calculator = LawnCareCalculator(region)
    
    # Initialize crab grass knowledge base if needed
    crab_kb = None
    if args.crabgrass or args.identify or args.treatment or args.prevention or args.lifecycle or args.calendar:
        crab_kb = CrabGrassKnowledgeBase(region)
    
    print(f"Lawn Care Calculator - {region.value.title()} Region")
    print("=" * 50)
    
    # Handle crab grass knowledge base commands first
    if args.crabgrass:
        show_crabgrass_overview(crab_kb)
    elif args.identify:
        identify_crabgrass(crab_kb, args.identify)
    elif args.treatment:
        show_crabgrass_treatments(crab_kb, args.month or datetime.now().month)
    elif args.prevention:
        show_crabgrass_prevention(crab_kb)
    elif args.lifecycle:
        show_crabgrass_lifecycle(crab_kb)
    elif args.calendar:
        show_crabgrass_calendar(crab_kb)
    # Handle regular lawn care commands
    elif args.schedule:
        show_yearly_schedule(calculator)
    
    elif args.activity:
        show_activity_info(calculator, LawnCareActivity(args.activity))
    
    elif args.current_optimal:
        if not args.month or args.temp is None:
            print("Error: --current-optimal requires both --month and --temp")
            sys.exit(1)
        check_current_optimal(calculator, args.month, args.temp)
    
    elif args.next_window:
        show_next_window(calculator, LawnCareActivity(args.next_window))
    
    elif args.month:
        show_monthly_activities(calculator, args.month)
    
    else:
        # Default: show overview
        show_overview(calculator)


def show_yearly_schedule(calculator):
    """Display the complete yearly schedule"""
    print("\nYearly Lawn Care Schedule:")
    print("-" * 30)
    
    month_names = ["", "January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]
    
    schedule = calculator.get_monthly_schedule()
    for month, activities in schedule.items():
        print(f"\n{month_names[month]}:")
        if activities:
            for activity in activities:
                window = calculator.get_timing_window(LawnCareActivity(activity))
                print(f"  • {activity.replace('_', ' ').title()}")
                print(f"    Temp: {window.optimal_temp_min}°F - {window.optimal_temp_max}°F")
        else:
            print("  • No scheduled activities")


def show_activity_info(calculator, activity):
    """Show detailed information for a specific activity"""
    window = calculator.get_timing_window(activity)
    next_window = calculator.get_next_optimal_window(activity)
    
    print(f"\n{activity.value.replace('_', ' ').title()} Information:")
    print("-" * 40)
    print(f"Optimal Months: {window.start_month} to {window.end_month}")
    print(f"Temperature Range: {window.optimal_temp_min}°F - {window.optimal_temp_max}°F")
    print(f"Description: {window.description}")
    print(f"\nNext Window: {next_window['start_date']} to {next_window['end_date']}")
    print(f"Days Until Start: {next_window['days_until_start']}")
    print(f"Window Length: {next_window['window_length_days']} days")


def check_current_optimal(calculator, month, temp):
    """Check if current conditions are optimal for all activities"""
    print(f"\nOptimal Activities for Month {month} at {temp}°F:")
    print("-" * 45)
    
    optimal_found = False
    for activity in LawnCareActivity:
        if calculator.is_optimal_time(activity, month, temp):
            print(f"✅ {activity.value.replace('_', ' ').title()}")
            optimal_found = True
        else:
            window = calculator.get_timing_window(activity)
            # Check what's preventing optimization
            month_ok = window.start_month <= month <= window.end_month
            temp_ok = window.optimal_temp_min <= temp <= window.optimal_temp_max
            
            if not month_ok and not temp_ok:
                reason = f"wrong month ({window.start_month}-{window.end_month}) and temperature ({window.optimal_temp_min}-{window.optimal_temp_max}°F)"
            elif not month_ok:
                reason = f"wrong month (optimal: {window.start_month}-{window.end_month})"
            else:
                reason = f"wrong temperature (optimal: {window.optimal_temp_min}-{window.optimal_temp_max}°F)"
            
            print(f"❌ {activity.value.replace('_', ' ').title()} - {reason}")
    
    if not optimal_found:
        print("No activities are optimal for these conditions.")


def show_next_window(calculator, activity):
    """Show the next optimal window for a specific activity"""
    window_info = calculator.get_next_optimal_window(activity)
    
    print(f"\nNext {activity.value.replace('_', ' ').title()} Window:")
    print("-" * 40)
    print(f"Start: {window_info['start_date']}")
    print(f"End: {window_info['end_date']}")
    print(f"Days Until: {window_info['days_until_start']}")
    print(f"Duration: {window_info['window_length_days']} days")
    print(f"Optimal Temperature: {window_info['optimal_temp_range']}")
    print(f"Notes: {window_info['description']}")


def show_monthly_activities(calculator, month):
    """Show all optimal activities for a specific month"""
    month_names = ["", "January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]
    
    activities = calculator.get_all_activities_for_month(month)
    
    print(f"\nOptimal Activities for {month_names[month]}:")
    print("-" * 35)
    
    if activities:
        for activity in activities:
            window = calculator.get_timing_window(activity)
            print(f"• {activity.value.replace('_', ' ').title()}")
            print(f"  Temperature: {window.optimal_temp_min}°F - {window.optimal_temp_max}°F")
            print(f"  Notes: {window.description}")
            print()
    else:
        print("No activities are optimal for this month.")


def show_overview(calculator):
    """Show a general overview of the calculator"""
    print("\nLawn Care Calculator Overview:")
    print("-" * 35)
    print(f"Region: {calculator.region.value.title()}")
    print(f"Current Date: {datetime.now().strftime('%Y-%m-%d')}")
    
    # Show current month activities
    current_month = datetime.now().month
    current_activities = calculator.get_all_activities_for_month(current_month)
    
    print(f"\nActivities for Current Month:")
    if current_activities:
        for activity in current_activities:
            print(f"  • {activity.value.replace('_', ' ').title()}")
    else:
        print("  • No activities optimal for current month")
    
    print(f"\nUse --help to see all available options")
    print("Examples:")
    print("  python cli.py --schedule")
    print("  python cli.py --crabgrass")
    print("  python cli.py --identify 'wide leaves' 'finger-like seed heads'")


def show_crabgrass_overview(kb):
    """Show crab grass knowledge base overview"""
    print("\nCrab Grass Knowledge Base")
    print("=" * 30)
    print("Available commands:")
    print("  --identify: Identify crab grass type based on features")
    print("  --treatment: Get treatment recommendations")
    print("  --prevention: Show prevention strategies")
    print("  --lifecycle: Show lifecycle information")
    print("  --calendar: Show seasonal management calendar")
    
    # Show identification guide summary
    print("\nQuick Identification:")
    guide = kb.get_identification_guide()
    for grass_type, features in guide.items():
        print(f"\n{grass_type.replace('_', ' ').title()}:")
        for feature in features[:2]:  # Show first 2 features
            print(f"  • {feature['feature']}: {feature['description']}")


def identify_crabgrass(kb, observed_features):
    """Identify crab grass based on observed features"""
    print(f"\nCrab Grass Identification")
    print("-" * 30)
    print(f"Analyzing features: {', '.join(observed_features)}")
    
    result = kb.identify_crab_grass(observed_features)
    
    print(f"\nIdentification Result:")
    print(f"Most Likely Type: {result['likely_type']}")
    print(f"Confidence: {result['confidence']}")
    
    if result['matching_features']:
        print(f"\nMatching Features:")
        for grass_type, features in result['matching_features'].items():
            if features:
                print(f"  {grass_type}: {', '.join(features)}")
    
    # Show treatment recommendations
    current_month = datetime.now().month
    treatments = kb.get_treatment_recommendations(current_month)
    if treatments:
        print(f"\nRecommended Treatments for Current Month:")
        for treatment in treatments[:2]:  # Show top 2
            print(f"  • {treatment['name']} (Effectiveness: {treatment['effectiveness']}/10)")


def show_crabgrass_treatments(kb, month):
    """Show crab grass treatment recommendations"""
    print(f"\nCrab Grass Treatments for Month {month}")
    print("-" * 40)
    
    treatments = kb.get_treatment_recommendations(month)
    
    if treatments:
        for i, treatment in enumerate(treatments, 1):
            timing_match = "✅" if treatment['timing_match'] else "⏰"
            stage_match = "✅" if treatment['stage_appropriate'] else "❌"
            
            print(f"\n{i}. {treatment['name']}")
            print(f"   Type: {treatment['type'].replace('_', ' ').title()}")
            print(f"   Effectiveness: {treatment['effectiveness']}/10")
            print(f"   Cost: {treatment['cost_range']}")
            print(f"   Timing Match: {timing_match} | Stage Appropriate: {stage_match}")
            print(f"   Notes: {treatment['application_notes']}")
    else:
        print("No treatments recommended for this month.")


def show_crabgrass_prevention(kb):
    """Show crab grass prevention strategies"""
    print(f"\nCrab Grass Prevention Strategies")
    print("-" * 35)
    
    strategies = kb.get_prevention_strategies()
    
    for i, strategy in enumerate(strategies, 1):
        print(f"\n{i}. {strategy['strategy']}")
        print(f"   Description: {strategy['description']}")
        print(f"   Implementation: {strategy['implementation']}")
        print(f"   Effectiveness: {strategy['effectiveness']}")


def show_crabgrass_lifecycle(kb):
    """Show crab grass lifecycle information"""
    print(f"\nCrab Grass Lifecycle")
    print("-" * 25)
    
    lifecycle = kb.get_lifecycle_info()
    
    for stage, info in lifecycle.items():
        print(f"\n{stage.replace('_', ' ').title()}:")
        print(f"  Description: {info['description']}")
        print(f"  Timing: {info['timing']}")
        print(f"  Vulnerability: {info['vulnerability']}")
        print(f"  Treatment Window: {info['treatment_window']}")


def show_crabgrass_calendar(kb):
    """Show seasonal crab grass management calendar"""
    print(f"\nSeasonal Crab Grass Management Calendar")
    print("-" * 45)
    
    calendar = kb.get_seasonal_calendar()
    
    for season, activities in calendar.items():
        print(f"\n{season}:")
        for activity in activities:
            print(f"  • {activity}")


if __name__ == '__main__':
    main()