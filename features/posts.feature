@posts
Feature: Posts API
  As a client developer, I want to make sure "/posts" API endpoint can provide the expected data.

  Scenario: Get all posts
    Given client request all posts
    Then verify response contain posts


  Scenario Outline: Create a new post in supported languages
    Given client create new post with <title> and <body>
    Then verify new post created with expected <title> and <body>

    Examples: Title & Body
      | title               | body                                       |
      | English Title       | English text for new post                  |
      | Title with Emoji 😎 | English text for new post with Emoji ❤️    |
      | 日本語のタイトル       | 投稿テストの日本語テキスト                      |
      | Título en español   | Texto en español para probar publicaciones |


  Scenario: Block post creation without title & body
    Given client create new post with missing data
    Then verify new post failed to create