@auth
Feature: Authentication
  As a client developer, I want to ensure the authentication endpoints
  (login, refresh, me) function correctly.

  Scenario: User is able to authenticate
    Given user Emily is authenticated
    Then login schema should be valid
    And login data is valid

  Scenario: Authenticated user is able to fetch profile
    Given user Michael is authenticated
    When fetching user profile
    Then user profile schema should be valid
    And user profile data is valid

  Scenario: User unable to login without password
    When Emily attempts to login with missing password
    Then login error schema should be valid
    Then login error message should be Username and password required

  Scenario: User unable to login with incorrect password
    When Michael attempts to login with bad!pass password
    Then login error schema should be valid
    Then login error message should be Username is not valid
