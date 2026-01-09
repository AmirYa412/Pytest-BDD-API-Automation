@products
Feature: Products
  As a client developer, I want to ensure the products endpoints
  function correctly for listing, searching, and retrieving product details.

  Scenario: Get all products with default pagination
    When fetching all products
    Then products list schema should be valid
    And products list contains items

  Scenario Outline: Get all products with custom pagination, limit and sort
    When fetching products with limit 3, skip 5 and sort by <field> <order>
    Then products list schema should be valid
    And products list has 3 items, skipped 5 and sorted by <field> <order>

  Examples:
    | field | order |
    | title | asc   |
    | price | desc  |

  Scenario: Get single product details from list
    When fetching products with limit 2, skip 1 and sort by title desc
    And fetching product at index 1 from list
    Then product schema should be valid
    And product data is valid

  Scenario: Get product with invalid ID returns 404
    When fetching product with invalid ID 999999
    Then product error schema should be valid
    And error message contains not found

  Scenario: Search products and get details
    When searching products with query phone
    And fetching product at index 0 from search results
    Then product schema should be valid
    And product data is valid

  Scenario: Get products by category
    When fetching products in category smartphones
    Then products list schema should be valid
    And all products are in category smartphones