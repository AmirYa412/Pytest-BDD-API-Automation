@carts
Feature: Carts
  As a client developer, I want to ensure the carts endpoints
  function correctly for CRUD operations and cart management.

  Scenario: Create new cart with products from list
    Given user Emily is authenticated
    When fetching all products
    And creating cart with product at index 0 and quantity 2
    Then cart schema should be valid
    And cart data is valid
    And cart belongs to authenticated user

  Scenario: Get cart by ID from all carts
    When fetching all carts
    And fetching cart at index 0 from carts list
    Then cart schema should be valid
    And cart data is valid

  Scenario: Update cart from carts list
    When fetching all carts
    And updating cart at index 0 with product 5 and quantity 10
    Then update cart schema should be valid
    And cart contains product 5 with quantity 10

  Scenario: Delete cart from carts list
    When fetching all carts
    And deleting cart at index 1
    Then delete cart schema should be valid
    And cart is marked as deleted
