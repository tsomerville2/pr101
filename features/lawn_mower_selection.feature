Feature: Lawn Mower Selection and Visualization
  As a homeowner
  I want to select or type in what type of lawn mower I have
  And see a picture of my lawn mower model
  So that I can easily identify and get relevant information about my equipment

  Background:
    Given I am on the lawn mower selection page

  Scenario: Select lawn mower from dropdown list
    When I click on the lawn mower type dropdown
    Then I should see a list of available lawn mower types
    And the list should include "Push Mower"
    And the list should include "Self-Propelled Mower"
    And the list should include "Riding Mower"
    And the list should include "Zero-Turn Mower"
    And the list should include "Robotic Mower"

  Scenario: Select a specific lawn mower type from dropdown
    When I select "Riding Mower" from the dropdown
    Then the selected lawn mower type should be "Riding Mower"
    And I should see a picture of a riding mower
    And the picture should be clearly visible
    And the picture should be relevant to riding mowers

  Scenario: Type in custom lawn mower model
    When I type "Honda HRX217VKA" in the lawn mower input field
    And I press enter or click search
    Then the system should recognize "Honda HRX217VKA" as a valid model
    And I should see a picture of the Honda HRX217VKA mower
    And the picture should match the specific model entered

  Scenario: Type in partial lawn mower information
    When I type "Craftsman push" in the lawn mower input field
    And I press enter or click search
    Then I should see suggestions for Craftsman push mowers
    And I should see a representative picture of Craftsman push mowers
    And I should be able to select a specific model from the suggestions

  Scenario: Handle unknown lawn mower model
    When I type "UnknownBrand Model123" in the lawn mower input field
    And I press enter or click search
    Then I should see a message indicating the model is not recognized
    And I should see a generic lawn mower picture as fallback
    And I should be offered suggestions for similar models

  Scenario: Clear lawn mower selection
    Given I have selected "Zero-Turn Mower" from the dropdown
    And I can see a picture of a zero-turn mower
    When I click the clear or reset button
    Then the lawn mower selection should be cleared
    And the picture should be hidden or show a placeholder

  Scenario Outline: Select different lawn mower types and verify images
    When I select "<mower_type>" from the dropdown
    Then I should see a picture of a <mower_type>
    And the picture should be appropriate for the <mower_type> category

    Examples:
      | mower_type           |
      | Push Mower          |
      | Self-Propelled Mower |
      | Riding Mower        |
      | Zero-Turn Mower     |
      | Robotic Mower       |

  Scenario: Autocomplete functionality for typed input
    When I start typing "Hon" in the lawn mower input field
    Then I should see autocomplete suggestions
    And the suggestions should include models starting with "Honda"
    When I select "Honda" from the autocomplete
    Then I should see Honda-specific models
    And I should see a Honda lawn mower picture

  Scenario: Save selected lawn mower preference
    Given I have selected "Self-Propelled Mower" from the dropdown
    And I can see a picture of a self-propelled mower
    When I click the save or remember button
    Then my lawn mower selection should be saved
    And when I return to the page later
    Then "Self-Propelled Mower" should still be selected
    And the corresponding picture should still be displayed