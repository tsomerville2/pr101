Feature: Lawn Mower Selection and Visualization (Simplified)
  As a homeowner
  I want to select or type in my lawn mower type
  And see a picture of my lawn mower
  So I can easily identify and learn about my equipment

  Background:
    Given I am on the lawn mower selection page

  Scenario: Select lawn mower from dropdown and see picture
    When I select "Riding Mower" from the dropdown
    Then I should see a picture of a riding mower

  Scenario: Type in specific lawn mower model and see picture
    When I type "Honda HRX217VKA" in the lawn mower input field
    And I press enter
    Then I should see a picture of the Honda HRX217VKA mower

  Scenario: Save and retain selected lawn mower preference
    Given I have selected "Self-Propelled Mower" from the dropdown
    When I click the save button
    And I return to the page later
    Then "Self-Propelled Mower" should still be selected
    And the picture should still be displayed
