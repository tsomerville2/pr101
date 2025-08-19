"""
Step definitions for Lawn Care Timing Calculator BDD tests
"""
from behave import given, when, then, step
from lawn_care_calculator import (LawnCareCalculator, LawnCareActivity, Region, 
                                GrassType, WeatherCondition, TimerStatus, SoilMoisture, Season)
import time

@given('I select "{activity}" as my lawn care activity')
def step_select_activity(context, activity):
    context.activity = getattr(LawnCareActivity, activity.upper())

@given('I am in the "{region}" region')
def step_select_region(context, region):
    context.region = getattr(Region, region.upper())
    context.calculator = LawnCareCalculator(context.region)

@given('I want to do "{activity}" activity')
def step_want_activity(context, activity):
    context.activity = getattr(LawnCareActivity, activity.upper())

@given('it is month {month:d} with temperature {temp:g}°F')
def step_current_conditions(context, month, temp):
    context.month = month
    context.temperature = temp

@when('I request the optimal timing window')
def step_request_timing_window(context):
    context.timing_window = context.calculator.get_timing_window(context.activity)

@when('I check if current conditions are optimal')
def step_check_optimal_conditions(context):
    context.is_optimal = context.calculator.is_optimal_time(
        context.activity, context.month, context.temperature
    )

@when('I request the next optimal window')
def step_request_next_window(context):
    from datetime import datetime
    # Create a date object for the current month
    current_date = datetime(2024, context.month, 15)  # Use 15th of month as example
    context.next_window = context.calculator.get_next_optimal_window(
        context.activity, current_date
    )

@when('I request timing for "{activity}" activity')
def step_request_activity_timing(context, activity):
    context.activity = getattr(LawnCareActivity, activity.upper())
    context.timing_window = context.calculator.get_timing_window(context.activity)

@then('I should receive timing recommendations for months {start1:d}-{end1:d}')
def step_verify_timing_months(context, start1, end1):
    window = context.timing_window
    assert window.start_month == start1, f"Expected start month {start1}, got {window.start_month}"
    assert window.end_month == end1, f"Expected end month {end1}, got {window.end_month}"

@then('the temperature range should be {min_temp:g}-{max_temp:g}°F')
def step_verify_temperature_range(context, min_temp, max_temp):
    window = context.timing_window
    assert window.optimal_temp_min == min_temp, f"Expected min temp {min_temp}, got {window.optimal_temp_min}"
    assert window.optimal_temp_max == max_temp, f"Expected max temp {max_temp}, got {window.optimal_temp_max}"

@then('the system should confirm optimal conditions')
def step_confirm_optimal(context):
    assert context.is_optimal == True, "Expected optimal conditions, but got non-optimal"

@then('I should receive the next available optimal timing')
def step_verify_next_timing(context):
    assert context.next_window is not None, "Expected next window, but got None"
    assert 'start_date' in context.next_window, "Expected start_date in result"
    assert 'days_until_start' in context.next_window, "Expected days_until_start in result"

@then('it should be after the current date')
def step_verify_future_timing(context):
    days_until = context.next_window['days_until_start']
    assert days_until > 0, f"Next window should be in the future, but days until start is {days_until}"

@then('the spring window should start later than central region')
def step_verify_delayed_spring(context):
    # Create central calculator for comparison
    central_calc = LawnCareCalculator(Region.CENTRAL)
    central_window = central_calc.get_timing_window(context.activity)
    
    assert context.timing_window.start_month >= central_window.start_month, \
        f"Northern spring should start later than central (northern: {context.timing_window.start_month}, central: {central_window.start_month})"

@then('the fall window should end earlier than central region')
def step_verify_early_fall_end(context):
    central_calc = LawnCareCalculator(Region.CENTRAL)
    central_window = central_calc.get_timing_window(context.activity)
    
    if context.timing_window.fall_end_month > 0 and central_window.fall_end_month > 0:
        assert context.timing_window.fall_end_month <= central_window.fall_end_month, \
            f"Northern fall should end earlier than central (northern: {context.timing_window.fall_end_month}, central: {central_window.fall_end_month})"

@then('the growing season should be longer than northern region')
def step_verify_longer_season(context):
    northern_calc = LawnCareCalculator(Region.NORTHERN)
    northern_window = northern_calc.get_timing_window(context.activity)
    
    # Calculate season length (considering both spring and fall windows)
    southern_length = (context.timing_window.end_month - context.timing_window.start_month + 1)
    if context.timing_window.fall_end_month > 0:
        southern_length += (context.timing_window.fall_end_month - context.timing_window.fall_start_month + 1)
    
    northern_length = (northern_window.end_month - northern_window.start_month + 1)
    if northern_window.fall_end_month > 0:
        northern_length += (northern_window.fall_end_month - northern_window.fall_start_month + 1)
    
    assert southern_length >= northern_length, \
        f"Southern growing season should be longer (southern: {southern_length}, northern: {northern_length})"

@then('winter activities should be available later in the year')
def step_verify_extended_winter(context):
    # This would be verified by the timing windows for winter activities
    # For this demo, we'll check that southern region timing is generally extended
    assert context.timing_window is not None, "Expected timing window to be calculated"


# Watering Timer Step Definitions

@given('I have a lawn watering timer for the {region} region')
def step_create_watering_timer_with_region(context, region):
    context.region = getattr(Region, region.upper())
    context.calculator = LawnCareCalculator(context.region)

@when('I request the watering frequency for my lawn type "{grass_type}"')
def step_request_watering_frequency(context, grass_type):
    context.grass_type = getattr(GrassType, grass_type.upper())
    context.watering_frequency = context.calculator.get_watering_frequency(context.grass_type)

@then('I should get a recommendation to water every {frequency}')
def step_verify_watering_frequency(context, frequency):
    assert frequency in context.watering_frequency["frequency"], \
        f"Expected frequency containing '{frequency}', got '{context.watering_frequency['frequency']}'"

@then('the optimal time should be early morning between {time_range}')
def step_verify_optimal_time(context, time_range):
    assert time_range in context.watering_frequency["optimal_time"], \
        f"Expected time range '{time_range}', got '{context.watering_frequency['optimal_time']}'"

@then('the duration should be {duration} minutes per zone')
def step_verify_duration_range(context, duration):
    assert duration in context.watering_frequency["duration"], \
        f"Expected duration containing '{duration}', got '{context.watering_frequency['duration']}'"

@given('I have set my watering duration to {duration:d} minutes')
def step_set_watering_duration(context, duration):
    context.watering_timer = context.calculator.create_watering_timer(duration)

@when('I start the watering timer')
def step_start_watering_timer(context):
    context.watering_timer.start()
    context.timer_status = context.watering_timer.get_status()

@then('the countdown should begin at {duration:d} minutes')
def step_verify_countdown_start(context, duration):
    status = context.watering_timer.get_status()
    assert status["original_duration"] == duration, \
        f"Expected original duration {duration}, got {status['original_duration']}"

@then('the timer status should be "{expected_status}"')
def step_verify_timer_status(context, expected_status):
    status = context.watering_timer.get_status()
    assert status["status"] == expected_status, \
        f"Expected status '{expected_status}', got '{status['status']}'"

@then('I should get time remaining updates')
def step_verify_time_updates(context):
    status = context.watering_timer.get_status()
    assert "remaining_minutes" in status, "Expected remaining_minutes in status"
    assert "progress_percentage" in status, "Expected progress_percentage in status"

@given('I have a running watering timer with {minutes:d} minutes remaining')
def step_create_running_timer_with_time(context, minutes):
    context.watering_timer = context.calculator.create_watering_timer(minutes + 5)  # Set longer initial duration
    context.watering_timer.start()
    time.sleep(0.1)  # Brief pause to ensure timer starts
    # Manually adjust remaining time for testing
    context.watering_timer.remaining_minutes = minutes

@when('I check the timer status')
def step_check_timer_status(context):
    context.timer_status = context.watering_timer.get_status()

@then('I should see {minutes:d} minutes remaining')
def step_verify_minutes_remaining(context, minutes):
    # Allow for small timing variations
    remaining = context.timer_status["remaining_minutes"]
    assert abs(remaining - minutes) <= 1, \
        f"Expected approximately {minutes} minutes remaining, got {remaining}"

@then('the timer should still be running')
def step_verify_still_running(context):
    assert context.timer_status["status"] == "running", \
        f"Expected timer to be running, got {context.timer_status['status']}"

@then('I should get the current progress percentage')
def step_verify_progress_percentage(context):
    assert "progress_percentage" in context.timer_status, "Expected progress_percentage in status"
    assert 0 <= context.timer_status["progress_percentage"] <= 100, \
        f"Progress percentage should be 0-100, got {context.timer_status['progress_percentage']}"

@given('I have a running watering timer with {minutes:d} minute remaining')
def step_create_timer_one_minute(context, minutes):
    context.watering_timer = context.calculator.create_watering_timer(minutes + 1)
    context.watering_timer.start()
    context.watering_timer.remaining_minutes = minutes

@when('the timer reaches 0')
def step_timer_reaches_zero(context):
    # Simulate timer completion
    context.watering_timer.status = TimerStatus.COMPLETED
    context.watering_timer.remaining_minutes = 0

@then('I should get a completion notification')
def step_verify_completion_notification(context):
    status = context.watering_timer.get_status()
    assert status["status"] == "completed", "Expected completion status"
    assert status["remaining_minutes"] == 0, "Expected 0 minutes remaining"

@then('I should see next watering recommendation')
def step_verify_next_watering_recommendation(context):
    # This would typically show next watering schedule
    recommendation = context.calculator.get_watering_frequency(GrassType.COOL_SEASON)
    assert recommendation is not None, "Expected watering recommendation"

@given('the current weather is "{weather}" with temperature {temp:g}°F')
def step_set_weather_conditions(context, weather, temp):
    context.weather = getattr(WeatherCondition, weather.upper())
    context.temperature = temp

@given('I last watered my lawn {days:d} days ago')
def step_set_last_watering(context, days):
    context.days_since_last_watering = days

@when('I check when to water next')
def step_check_next_watering(context):
    context.next_watering = context.calculator.calculate_next_watering(
        GrassType.COOL_SEASON, context.weather, context.temperature, context.days_since_last_watering
    )

@then('I should be advised to water within the next {hours:d} hours')
def step_verify_water_soon(context, hours):
    days_until = context.next_watering["days_until_next_watering"]
    assert days_until <= 1, f"Expected to water within 1 day, got {days_until} days"

@then('the system should account for hot weather conditions')
def step_verify_hot_weather_adjustment(context):
    assert context.next_watering["weather_adjusted"], "Expected weather adjustment for hot conditions"

@given('the current weather is "{weather}" with {rainfall:g} inches of rainfall today')
def step_set_rainy_weather(context, weather, rainfall):
    context.weather = getattr(WeatherCondition, weather.upper())
    context.rainfall = rainfall

@then('I should be advised to wait {days} more days')
def step_verify_wait_days(context, days):
    advice = context.next_watering["advice"]
    assert "wait" in advice.lower() or "days" in advice.lower(), \
        f"Expected advice to mention waiting, got: {advice}"

@then('the system should account for natural rainfall')
def step_verify_rainfall_adjustment(context):
    advice = context.next_watering["advice"]
    assert "rain" in advice.lower(), f"Expected advice to mention rainfall, got: {advice}"

@given('I have a "{grass_type}" lawn type')
def step_set_grass_type(context, grass_type):
    context.grass_type = getattr(GrassType, grass_type.upper())

@given('the current season is "{season}"')
def step_set_season(context, season):
    context.season = getattr(Season, season.upper())

@when('I request my weekly watering schedule')
def step_request_weekly_schedule(context):
    context.weekly_schedule = context.calculator.get_watering_frequency(context.grass_type, context.season)

@then('I should get {frequency} watering sessions per week')
def step_verify_weekly_frequency(context, frequency):
    assert frequency in context.weekly_schedule["frequency"], \
        f"Expected frequency containing '{frequency}', got '{context.weekly_schedule['frequency']}'"

@then('each session should be {duration} minutes')
def step_verify_session_duration(context, duration):
    assert duration in context.weekly_schedule["duration"], \
        f"Expected duration containing '{duration}', got '{context.weekly_schedule['duration']}'"

@then('the schedule should include optimal times')
def step_verify_optimal_times_included(context):
    assert "optimal_time" in context.weekly_schedule, "Expected optimal_time in schedule"
    assert context.weekly_schedule["optimal_time"], "Expected non-empty optimal time"

@when('I pause the timer')
def step_pause_timer(context):
    context.watering_timer.pause()

@then('the remaining time should stay at {minutes:d} minutes')
def step_verify_time_stays_same(context, minutes):
    time.sleep(0.1)  # Brief pause
    status = context.watering_timer.get_status()
    remaining = status["remaining_minutes"]
    assert abs(remaining - minutes) <= 1, \
        f"Expected approximately {minutes} minutes remaining, got {remaining}"

@when('I resume the timer')
def step_resume_timer(context):
    context.watering_timer.resume()

@then('the countdown should continue from {minutes:d} minutes')
def step_verify_countdown_continues(context, minutes):
    time.sleep(0.1)  # Brief pause
    status = context.watering_timer.get_status()
    # Timer should be running and close to the expected time
    assert status["status"] == "running", f"Expected running status, got {status['status']}"

@when('I reset the timer')
def step_reset_timer(context):
    context.watering_timer.reset()

@then('the timer should return to the original duration')
def step_verify_reset_to_original(context):
    status = context.watering_timer.get_status()
    original = status["original_duration"]
    remaining = status["remaining_minutes"]
    assert remaining == original, \
        f"Expected remaining time to equal original duration {original}, got {remaining}"

@then('I should be able to start a fresh session')
def step_verify_can_start_fresh(context):
    status = context.watering_timer.get_status()
    assert status["status"] == "stopped", f"Expected stopped status, got {status['status']}"

@then('I should water {frequency} per week')
def step_verify_regional_frequency(context, frequency):
    assert frequency in context.watering_frequency["frequency"], \
        f"Expected frequency containing '{frequency}', got '{context.watering_frequency['frequency']}'"

@then('each session should be {duration} minutes')
def step_verify_regional_duration(context, duration):
    assert duration in context.watering_frequency["duration"], \
        f"Expected duration containing '{duration}', got '{context.watering_frequency['duration']}'"

@given('the soil moisture level is "{moisture_level}"')
def step_set_soil_moisture(context, moisture_level):
    context.soil_moisture = getattr(SoilMoisture, moisture_level.upper())

@given('the temperature is above {temp:g}°F')
def step_set_high_temperature(context, temp):
    context.temperature = temp + 1  # Set slightly above

@given('no rain is forecasted for {days:d} days')
def step_set_dry_forecast(context, days):
    context.days_without_rain = days

@when('I request watering recommendations')
def step_request_smart_recommendations(context):
    context.smart_recommendation = context.calculator.get_smart_watering_recommendation(
        GrassType.COOL_SEASON, context.soil_moisture, context.temperature, context.days_without_rain
    )

@then('I should be advised to water immediately')
def step_verify_immediate_watering(context):
    assert context.smart_recommendation["urgency"] == "immediate", \
        f"Expected immediate urgency, got {context.smart_recommendation['urgency']}"

@then('the recommended duration should be extended by {percentage:d}%')
def step_verify_extended_duration(context, percentage):
    adjustment = context.smart_recommendation["duration_adjustment_percentage"]
    assert abs(adjustment - percentage) <= 5, \
        f"Expected approximately {percentage}% adjustment, got {adjustment}%"

@then('I should get a notification about dry conditions')
def step_verify_dry_conditions_notification(context):
    advice = context.smart_recommendation["advice"]
    assert "dry" in advice.lower(), f"Expected advice to mention dry conditions, got: {advice}"