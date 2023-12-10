@comments
Feature: Comments
  As a client developer, I want to make sure "/comments" & "/posts/*/comments" API endpoints working as expected.
  The client should be able to fetch and create new posts via API requests.

  Scenario: Get random post's comments
    Given client request all posts
    When client choose a random post
    And client request comments of a post
    Then verify post contain comments

  Scenario Outline: Publish new comment on random post
    Given client request all posts
    When client choose a random post
    And client publish new comment with <name>, <email> and <body>
    Then verify new comment published with <name>, <email> and <body>

    Examples:  Name, Email & Body
      | name     | email             | body                              |
      | John Doe | johndoe@gmail.com | Body text for new comment test    |
      | Foo Boy  | foo@gmail.com     | Body t3xt w!th sp3ci@l ch@r@cters |
