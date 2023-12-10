@comments
Feature: Comments
  As a client developer, I want to make sure "/posts/*/comments" API endpoint working as expected.

  Scenario: Get random post's comments
    Given client request all posts
    When client choose a random post
    And client request comments of a post
    Then verify post contain comments