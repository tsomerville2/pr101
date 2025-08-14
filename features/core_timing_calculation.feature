Feature: Core Timing Calculation
  As a homeowner
  I want to calculate optimal timing for lawn care activities
  So that my lawn care efforts are most effective

  Scenario: Calculate optimal timing window for seeding
    Given I select "seeding" as my lawn care activity
    And I am in the "central" region
    When I request the optimal timing window
    Then I should receive timing recommendations for months 4-6
    And the temperature range should be 55-80°F

  Scenario: Validate current conditions are optimal
    Given I want to do "fertilizing" activity
    And I am in the "northern" region
    And it is month 5 with temperature 70°F
    When I check if current conditions are optimal
    Then the system should confirm optimal conditions
    
  Scenario: Find next optimal window when conditions aren't met
    Given I want to do "overseeding" activity
    And I am in the "southern" region  
    And it is month 7 with temperature 95°F
    When I request the next optimal window
    Then I should receive the next available optimal timing
    And it should be after the current date