#!/usr/bin/env python3
"""
Simple test script for the watering timer functionality
"""

from lawn_care_calculator import (LawnCareCalculator, GrassType, WeatherCondition, 
                                SoilMoisture, Season, Region)
import time

def test_watering_frequency():
    """Test watering frequency recommendations"""
    print("Testing watering frequency recommendations...")
    
    calculator = LawnCareCalculator(Region.CENTRAL)
    
    # Test cool season grass
    frequency = calculator.get_watering_frequency(GrassType.COOL_SEASON)
    print(f"Cool season grass: {frequency}")
    assert "frequency" in frequency
    assert "duration" in frequency
    assert "optimal_time" in frequency
    
    # Test warm season grass in summer
    frequency_summer = calculator.get_watering_frequency(GrassType.WARM_SEASON, Season.SUMMER)
    print(f"Warm season grass in summer: {frequency_summer}")
    
    print("✓ Watering frequency tests passed")

def test_watering_timer():
    """Test watering timer functionality"""
    print("\nTesting watering timer...")
    
    calculator = LawnCareCalculator()
    
    # Create a timer
    timer = calculator.create_watering_timer(5)  # 5 minute timer for testing
    
    # Check initial status
    status = timer.get_status()
    print(f"Initial status: {status}")
    assert status["status"] == "stopped"
    assert status["remaining_minutes"] == 5
    assert status["progress_percentage"] == 0
    
    # Start the timer
    timer.start()
    time.sleep(0.1)  # Brief pause
    
    status = timer.get_status()
    print(f"Running status: {status}")
    assert status["status"] == "running"
    assert status["remaining_minutes"] <= 5
    
    # Pause the timer
    timer.pause()
    status = timer.get_status()
    print(f"Paused status: {status}")
    assert status["status"] == "paused"
    
    # Reset the timer
    timer.reset()
    status = timer.get_status()
    print(f"Reset status: {status}")
    assert status["status"] == "stopped"
    assert status["remaining_minutes"] == 5
    
    print("✓ Watering timer tests passed")

def test_smart_watering():
    """Test smart watering recommendations"""
    print("\nTesting smart watering recommendations...")
    
    calculator = LawnCareCalculator()
    
    # Test hot, dry conditions
    recommendation = calculator.get_smart_watering_recommendation(
        GrassType.COOL_SEASON, SoilMoisture.LOW, 85, 5
    )
    print(f"Hot, dry conditions: {recommendation}")
    assert recommendation["urgency"] == "immediate"
    assert recommendation["duration_adjustment_percentage"] > 0
    
    # Test normal conditions
    recommendation_normal = calculator.get_smart_watering_recommendation(
        GrassType.COOL_SEASON, SoilMoisture.MEDIUM, 70, 1
    )
    print(f"Normal conditions: {recommendation_normal}")
    
    print("✓ Smart watering tests passed")

def test_weather_based_watering():
    """Test weather-based watering calculations"""
    print("\nTesting weather-based watering...")
    
    calculator = LawnCareCalculator()
    
    # Test hot, sunny weather
    next_watering = calculator.calculate_next_watering(
        GrassType.COOL_SEASON, WeatherCondition.SUNNY, 85, 2
    )
    print(f"Hot, sunny weather: {next_watering}")
    assert next_watering["weather_adjusted"] == True
    
    # Test rainy weather
    next_watering_rain = calculator.calculate_next_watering(
        GrassType.COOL_SEASON, WeatherCondition.RAINY, 70, 1, rainfall_inches=0.6
    )
    print(f"Rainy weather: {next_watering_rain}")
    assert "rain" in next_watering_rain["advice"].lower()
    
    print("✓ Weather-based watering tests passed")

if __name__ == "__main__":
    print("Running Watering Timer Tests")
    print("=" * 40)
    
    try:
        test_watering_frequency()
        test_watering_timer()
        test_smart_watering()
        test_weather_based_watering()
        
        print("\n🎉 All tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        raise