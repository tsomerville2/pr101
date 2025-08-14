Feature: Regional Climate Variations
  As a user in different climate zones
  I want timing adjusted for my regional conditions
  So that recommendations match my local growing season

  Scenario: Northern region has delayed spring timing
    Given I am in the "northern" region
    When I request timing for "seeding" activity
    Then the spring window should start later than central region
    And the fall window should end earlier than central region

  Scenario: Southern region has extended growing season
    Given I am in the "southern" region
    When I request timing for "fertilizing" activity  
    Then the growing season should be longer than northern region
    And winter activities should be available later in the year