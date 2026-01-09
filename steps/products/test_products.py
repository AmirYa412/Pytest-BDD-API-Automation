from pytest_bdd import scenarios, then, parsers
from utilities.schema_validation import validate_schema
from services.products import Products, ProductGet

scenarios("../../features/products.feature")


# ====== Schema validation steps ======

@then("products list schema should be valid")
def verify_products_list_schema(products_response):
    """Validate products list response against schema."""
    validate_schema(products_response, Products.SCHEMA)


@then("product schema should be valid")
def verify_product_schema(product_response):
    """Validate single product response against schema."""
    validate_schema(product_response, ProductGet.SCHEMA)


@then("product error schema should be valid")
def verify_product_error_schema(product_error_response):
    """Validate 404 error response against schema."""
    validate_schema(product_error_response, ProductGet.ERROR_404_SCHEMA)


# ====== Response content validations ======

@then("products list contains items")
def verify_products_list_not_empty(products_response):
    """Verify the products list is not empty."""
    assert len(products_response["products"]) > 0, "Products list is empty"
    assert products_response["total"] > 0, "Total count should be greater than 0"


@then(parsers.parse("products list has {count:d} items, skipped {skip:d} and sorted by {field} {order}"))
def verify_products_pagination_and_sort(products_response, count, skip, field, order):
    """Verify the products list count, skip value, and sort order."""
    # Verify count & count
    actual_count = len(products_response["products"])
    assert actual_count == count, f"Expected {count} products, got {actual_count}"
    assert products_response["skip"] == skip, f"Expected skip={skip}, got {products_response['skip']}"

    # Verify sorting
    products = products_response["products"]
    assert len(products) > 1, "Need at least 2 products to verify sorting"
    values = [product[field] for product in products]
    if order == "asc":
        assert values == sorted(values), f"Products not sorted ascending by {field}: {values}"
    elif order == "desc":
        assert values == sorted(values, reverse=True), f"Products not sorted descending by {field}: {values}"


@then("product data is valid")
def verify_product_data(product_response):
    """Verify single product data logic and business rules."""
    # Price validation
    assert product_response["price"] > 0, "Product price must be positive"

    # Stock validation
    assert product_response["stock"] >= 0, "Stock cannot be negative"

    # String fields validation
    assert len(product_response["title"]) > 0, "Product title cannot be empty"
    assert len(product_response["description"]) > 0, "Product description cannot be empty"
    assert len(product_response["category"]) > 0, "Product category cannot be empty"

    # Rating validation
    assert 0 <= product_response["rating"] <= 5, f"Rating {product_response['rating']} out of valid range (0-5)"

    # Thumbnail validation
    assert product_response["thumbnail"].startswith("http"), "Thumbnail must be a valid URL"


@then(parsers.parse('error message contains {expected_text}'))
def verify_error_message_contains(product_error_response, expected_text):
    """Verify error message contains expected text."""
    actual_message = product_error_response.get("message", "")
    assert expected_text in actual_message, f"Expected message to contain '{expected_text}', got '{actual_message}'"


@then(parsers.parse('all products match search query "{query}"'))
def verify_search_results_match_query(products_response, query):
    """Verify all products in search results match the query."""
    query_lower = query.lower()
    products = products_response["products"]

    assert len(products) > 0, f"No products found for query '{query}'"

    for product in products:
        title = product["title"].lower()
        # Product title should contain the search query
        assert query_lower in title, f"Product '{product['title']}' does not match query '{query}'"


@then(parsers.parse('all products are in category {category}'))
def verify_products_category(products_response, category):
    """Verify all products belong to the specified category."""
    products = products_response["products"]

    assert len(products) > 0, f"No products found in category '{category}'"

    for product in products:
        actual_category = product["category"].lower()
        expected_category = category.lower()
        assert actual_category == expected_category, \
            f"Product '{product['title']}' is in category '{product['category']}', expected '{category}'"