#!/usr/bin/env python3
"""
Command-line interface for the Lawn Care Calculator
"""

import argparse
import sys
from datetime import datetime
from lawn_care_calculator import LawnCareCalculator, LawnCareActivity, Region
from height_analyzer import HeightAnalyzer


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
  python cli.py --height-scan photo.jpg --reference-object smartphone
  python cli.py --ssa-scan image.png --reference-height 85.6
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
    
    parser.add_argument('--height-scan', '--ssa-scan',
                       type=str,
                       help='Analyze height from photo (provide image path)')
    
    parser.add_argument('--reference-object',
                       choices=['credit_card', 'coin_quarter', 'smartphone', 'door', 'standard_brick'],
                       help='Reference object in photo for scale')
    
    parser.add_argument('--reference-height',
                       type=float,
                       help='Known height of reference object in mm')
    
    args = parser.parse_args()
    
    # Initialize calculator
    region = Region(args.region)
    calculator = LawnCareCalculator(region)
    
    print(f"Lawn Care Calculator - {region.value.title()} Region")
    print("=" * 50)
    
    # Handle different command modes
    if args.schedule:
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
    
    elif args.height_scan:
        analyze_height_from_photo(args.height_scan, args.reference_object, args.reference_height)
    
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


def analyze_height_from_photo(image_path, reference_object=None, reference_height=None):
    """Analyze height from a photo using ML techniques."""
    print("\nHeight Analysis from Photo")
    print("=" * 30)
    print(f"Image: {image_path}")
    
    try:
        analyzer = HeightAnalyzer()
        
        # Perform analysis
        result = analyzer.analyze_height_from_photo(
            image_path, reference_object, reference_height
        )
        
        if result.get("success"):
            print("\n✅ Analysis Complete!")
            print("-" * 20)
            print(f"Estimated Height: {result['height_cm']} cm")
            print(f"                 {result['height_inches']} inches")
            print(f"                 {result['height_feet_inches']}")
            print(f"Confidence Score: {result['confidence']:.0%}")
            print(f"Method Used: {result['method']}")
            
            if result['confidence'] >= 0.7:
                print("\n🎯 High confidence result!")
            elif result['confidence'] >= 0.5:
                print("\n⚠️  Moderate confidence - consider using a reference object")
            else:
                print("\n❌ Low confidence - try with better lighting or reference object")
            
            print(f"\nTechnical Details:")
            print(f"  Person height (pixels): {result['person_height_pixels']:.1f}")
            print(f"  Scale factor: {result['scale_factor']:.4f} mm/pixel")
            
        else:
            print(f"\n❌ Analysis Failed: {result.get('error', 'Unknown error')}")
            print("\nTips for better results:")
            print("• Ensure good lighting and clear image")
            print("• Include a reference object (credit card, smartphone, etc.)")
            print("• Make sure the person is fully visible")
            print("• Take photo from a reasonable distance")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure the image file exists and is a valid image format.")


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
    
    print(f"\n📏 NEW: Height Analysis Feature")
    print("  Use --height-scan to analyze height from photos!")
    print("  Example: python cli.py --height-scan photo.jpg --reference-object smartphone")
    
    print(f"\nUse --help to see all available options")
    print("Example: python cli.py --schedule")


if __name__ == '__main__':
    main()