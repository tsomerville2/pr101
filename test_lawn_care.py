#!/usr/bin/env python3
"""
Test suite for Lawn Care Calculator implementing BDD scenarios
"""

import unittest
from datetime import datetime
from lawn_care_calculator import LawnCareCalculator, LawnCareActivity, Region


class TestLawnCareCalculator(unittest.TestCase):
    """Test cases based on BDD scenarios from features/lawn_care_timing.feature"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.calculator = LawnCareCalculator(Region.CENTRAL)
    
    def test_seeding_window_timing(self):
        """Scenario: Calculate optimal seeding window"""
        window = self.calculator.get_timing_window(LawnCareActivity.SEEDING)
        
        self.assertEqual(window.start_month, 4, "Seeding should start in April")
        self.assertEqual(window.end_month, 6, "Seeding should end in June")
        self.assertEqual(window.optimal_temp_min, 55, "Min temp should be 55°F")
        self.assertEqual(window.optimal_temp_max, 80, "Max temp should be 80°F")
        self.assertIn("spring", window.description.lower(), "Should mention spring")
    
    def test_optimal_conditions_for_fertilizing(self):
        """Scenario: Check if current conditions are optimal for fertilizing"""
        # Test optimal conditions (May, 70°F)
        result = self.calculator.is_optimal_time(LawnCareActivity.FERTILIZING, 5, 70)
        self.assertTrue(result, "May with 70°F should be optimal for fertilizing")
    
    def test_non_optimal_conditions_for_winterizing(self):
        """Scenario: Check if current conditions are not optimal for winterizing"""
        # Test non-optimal conditions (June, 85°F)
        result = self.calculator.is_optimal_time(LawnCareActivity.WINTERIZING, 6, 85)
        self.assertFalse(result, "June with 85°F should not be optimal for winterizing")
    
    def test_next_optimal_window_overseeding(self):
        """Scenario: Get next optimal window for overseeding"""
        test_date = datetime(2024, 6, 15)
        window_info = self.calculator.get_next_optimal_window(LawnCareActivity.OVERSEEDING, test_date)
        
        start_date = datetime.strptime(window_info['start_date'], '%Y-%m-%d')
        self.assertEqual(start_date.month, 8, "Next overseeding window should start in August")
        self.assertGreaterEqual(window_info['window_length_days'], 30, "Window should be at least 30 days")
    
    def test_spring_peak_activities(self):
        """Scenario: Get activities for peak spring month (April)"""
        activities = self.calculator.get_all_activities_for_month(4)
        activity_values = [activity.value for activity in activities]
        
        self.assertIn('seeding', activity_values, "April should include seeding")
        self.assertIn('fertilizing', activity_values, "April should include fertilizing")
        self.assertIn('dethatching', activity_values, "April should include dethatching")
        self.assertIn('aeration', activity_values, "April should include aeration")
    
    def test_monthly_schedule_generation(self):
        """Scenario: Generate monthly schedule for the year"""
        schedule = self.calculator.get_monthly_schedule()
        
        # Test that we have all 12 months
        self.assertEqual(len(schedule), 12, "Should have schedule for all 12 months")
        
        # Test summer months include grub control
        summer_activities = schedule[7]  # July
        self.assertIn('grub_control', summer_activities, "Summer should include grub control")
        
        # Test fall months include overseeding
        fall_activities = schedule[9]  # September
        self.assertIn('overseeding', fall_activities, "Fall should include overseeding")
    
    def test_regional_timing_differences(self):
        """Scenario Outline: Regional timing differences"""
        test_cases = [
            (Region.NORTHERN, 4, 5),
            (Region.CENTRAL, 4, 6),
            (Region.SOUTHERN, 3, 5)
        ]
        
        for region, expected_start, expected_end in test_cases:
            with self.subTest(region=region):
                calc = LawnCareCalculator(region)
                window = calc.get_timing_window(LawnCareActivity.SEEDING)
                self.assertEqual(window.start_month, expected_start, 
                               f"{region.value} seeding should start in month {expected_start}")
                self.assertEqual(window.end_month, expected_end,
                               f"{region.value} seeding should end in month {expected_end}")
    
    def test_temperature_based_filtering(self):
        """Scenario: Temperature-based activity filtering"""
        # Get fertilizing window for reference
        window = self.calculator.get_timing_window(LawnCareActivity.FERTILIZING)
        optimal_month = window.start_month
        
        # Test temperature below minimum
        below_min_temp = window.optimal_temp_min - 5
        result = self.calculator.is_optimal_time(LawnCareActivity.FERTILIZING, optimal_month, below_min_temp)
        self.assertFalse(result, "Temperature below minimum should not be optimal")
    
    def test_year_boundary_winter_activities(self):
        """Scenario: Year boundary handling for winter activities"""
        southern_calc = LawnCareCalculator(Region.SOUTHERN)
        
        # Test December activities
        dec_activities = southern_calc.get_all_activities_for_month(12)
        dec_activity_values = [activity.value for activity in dec_activities]
        self.assertIn('winterizing', dec_activity_values, "December should include winterizing in southern regions")
        
        # Test January activities
        jan_activities = southern_calc.get_all_activities_for_month(1)
        jan_activity_values = [activity.value for activity in jan_activities]
        self.assertIn('winterizing', jan_activity_values, "January should include winterizing in southern regions")
    
    def test_calculator_initialization(self):
        """Test basic calculator initialization"""
        calc = LawnCareCalculator()
        self.assertEqual(calc.region, Region.CENTRAL, "Default region should be CENTRAL")
        
        calc_north = LawnCareCalculator(Region.NORTHERN)
        self.assertEqual(calc_north.region, Region.NORTHERN, "Should accept custom region")
    
    def test_all_activities_have_timing_data(self):
        """Ensure all activities have timing data for all regions"""
        for activity in LawnCareActivity:
            for region in Region:
                calc = LawnCareCalculator(region)
                window = calc.get_timing_window(activity)
                self.assertIsNotNone(window, f"Activity {activity.value} should have timing data for {region.value}")
                self.assertGreater(window.optimal_temp_max, window.optimal_temp_min, 
                                 f"Max temp should be greater than min temp for {activity.value}")


class TestLawnCareIntegration(unittest.TestCase):
    """Integration tests for the complete lawn care system"""
    
    def test_yearly_workflow_simulation(self):
        """Test a complete yearly workflow"""
        calculator = LawnCareCalculator(Region.CENTRAL)
        
        # Simulate checking each month
        yearly_activities = {}
        for month in range(1, 13):
            activities = calculator.get_all_activities_for_month(month)
            yearly_activities[month] = len(activities)
        
        # Verify we have activities throughout the year
        total_activities = sum(yearly_activities.values())
        self.assertGreater(total_activities, 0, "Should have activities throughout the year")
        
        # Verify peak seasons have more activities
        spring_activities = yearly_activities[4] + yearly_activities[5]  # April + May
        self.assertGreater(spring_activities, 0, "Spring should have lawn care activities")


def run_bdd_test_suite():
    """Run the BDD-style test suite and return results"""
    suite = unittest.TestLoader().loadTestsFromModule(__import__(__name__))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return {
        'tests_run': result.testsRun,
        'failures': len(result.failures),
        'errors': len(result.errors),
        'success': result.wasSuccessful()
    }


if __name__ == '__main__':
    print("Running Lawn Care Calculator BDD Test Suite")
    print("=" * 50)
    
    # Run the tests
    results = run_bdd_test_suite()
    
    print(f"\nTest Results Summary:")
    print(f"Tests run: {results['tests_run']}")
    print(f"Failures: {results['failures']}")
    print(f"Errors: {results['errors']}")
    print(f"Success: {results['success']}")
    
    if results['success']:
        print("\n✅ All BDD scenarios passed!")
    else:
        print(f"\n❌ {results['failures'] + results['errors']} test(s) failed")