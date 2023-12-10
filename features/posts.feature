@posts
Feature: Posts API
  As a client developer, I want to make sure "/posts" API endpoint functions correctly and returns expected data.
  The client should be able to fetch and create new posts via API requests.

  Scenario: Get all posts
    Given client request all posts
    Then verify response contain posts

  Scenario: Get random post and check it contain data
    Given client request all posts
    When client choose a random post
    Then verify post contain data

  Scenario Outline: Create a new post in supported languages
    Given client create new post with <title> and <body>
    Then verify new post created with expected <title> and <body>

    Examples: Title & Body
      | title               | body                                       |
      | English Title       | English text for new post                  |
      | Title with Emoji 😎 | English text for new post with Emoji ❤️    |
      | 日本語のタイトル       | 投稿テストの日本語テキスト                      |
      | Título en español   | Texto en español para probar publicaciones |

  Scenario: Bad request for new post creation without title & body
    Given client create new post with missing data
    Then verify new post failed to create