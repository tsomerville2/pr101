Feature: Lawn Care Best Window Timing Calculator
  As a homeowner
  I want to know the optimal timing for lawn care activities
  So that I can maintain a healthy lawn year-round

  Background:
    Given I have a lawn care calculator for the central region

  Scenario: Calculate optimal seeding window
    When I request the timing window for seeding
    Then I should get a window from April to June
    And the optimal temperature range should be 55°F to 80°F
    And the description should mention spring seeding

  Scenario: Check if current conditions are optimal for fertilizing
    Given the current month is 5
    And the current temperature is 70
    When I check if conditions are optimal for fertilizing
    Then the result should be true

  Scenario: Check if current conditions are not optimal for winterizing
    Given the current month is 6
    And the current temperature is 85
    When I check if conditions are optimal for winterizing
    Then the result should be false

  Scenario: Get next optimal window for overseeding
    Given the current date is 2024-06-15
    When I request the next optimal window for overseeding
    Then the start date should be in August
    And the window should be at least 30 days long

  Scenario: Get activities for peak spring month
    When I request all optimal activities for month 4
    Then the activities should include seeding
    And the activities should include fertilizing
    And the activities should include dethatching
    And the activities should include aeration

  Scenario: Generate monthly schedule for the year
    When I request the monthly schedule
    Then I should get activities for each month
    And summer months should include grub control
    And fall months should include overseeding

  Scenario Outline: Regional timing differences
    Given I have a lawn care calculator for the <region> region
    When I request the timing window for seeding
    Then the start month should be <start_month>
    And the end month should be <end_month>

    Examples:
      | region   | start_month | end_month |
      | northern | 4           | 5         |
      | central  | 4           | 6         |
      | southern | 3           | 5         |

  Scenario: Temperature-based activity filtering
    Given the current month is in the optimal range for fertilizing
    When the temperature is below the minimum optimal range
    Then the conditions should not be optimal for fertilizing

  Scenario: Year boundary handling for winter activities
    Given I have a lawn care calculator
    When I request activities for month 12
    Then winterizing should be included in southern regions
    When I request activities for month 1
    Then winterizing should be included in southern regions