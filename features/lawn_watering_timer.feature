Feature: Lawn Watering Timer with Countdown
  As a homeowner
  I want a timer to track how often I should water my lawn with countdown functionality
  So that I can maintain proper watering schedules and never miss watering sessions

  Background:
    Given I have a lawn watering timer for the central region

  Scenario: Get watering frequency recommendation
    When I request the watering frequency for my lawn type "cool_season"
    Then I should get a recommendation to water every 2-3 days
    And the optimal time should be early morning between 6-8 AM
    And the duration should be 15-20 minutes per zone

  Scenario: Start watering countdown timer
    Given I have set my watering duration to 20 minutes
    When I start the watering timer
    Then the countdown should begin at 20 minutes
    And the timer status should be "running"
    And I should get time remaining updates

  Scenario: Check time remaining during watering
    Given I have a running watering timer with 15 minutes remaining
    When I check the timer status
    Then I should see 15 minutes remaining
    And the timer should still be running
    And I should get the current progress percentage

  Scenario: Timer completion notification
    Given I have a running watering timer with 1 minute remaining
    When the timer reaches 0
    Then I should get a completion notification
    And the timer status should be "completed"
    And I should see next watering recommendation

  Scenario: Calculate next watering time based on weather
    Given the current weather is "sunny" with temperature 85°F
    And I last watered my lawn 2 days ago
    When I check when to water next
    Then I should be advised to water within the next 24 hours
    And the system should account for hot weather conditions

  Scenario: Calculate next watering time for rainy weather
    Given the current weather is "rainy" with 0.5 inches of rainfall today
    And I last watered my lawn 1 day ago
    When I check when to water next
    Then I should be advised to wait 2-3 more days
    And the system should account for natural rainfall

  Scenario: Get weekly watering schedule
    Given I have a "warm_season" lawn type
    And the current season is "summer"
    When I request my weekly watering schedule
    Then I should get 3-4 watering sessions per week
    And each session should be 25-30 minutes
    And the schedule should include optimal times

  Scenario: Pause and resume watering timer
    Given I have a running watering timer with 12 minutes remaining
    When I pause the timer
    Then the timer status should be "paused"
    And the remaining time should stay at 12 minutes
    When I resume the timer
    Then the timer status should be "running"
    And the countdown should continue from 12 minutes

  Scenario: Reset watering timer
    Given I have a running watering timer with 8 minutes remaining
    When I reset the timer
    Then the timer should return to the original duration
    And the timer status should be "stopped"
    And I should be able to start a fresh session

  Scenario Outline: Regional watering frequency differences
    Given I have a lawn watering timer for the <region> region
    And I have a <grass_type> lawn
    When I request the watering frequency
    Then I should water <frequency> per week
    And each session should be <duration> minutes

    Examples:
      | region   | grass_type   | frequency | duration |
      | northern | cool_season  | 2-3 times | 15-20    |
      | central  | cool_season  | 2-4 times | 20-25    |
      | southern | warm_season  | 3-4 times | 25-30    |

  Scenario: Smart watering recommendations with soil moisture
    Given the soil moisture level is "low"
    And the temperature is above 80°F
    And no rain is forecasted for 3 days
    When I request watering recommendations
    Then I should be advised to water immediately
    And the recommended duration should be extended by 25%
    And I should get a notification about dry conditions