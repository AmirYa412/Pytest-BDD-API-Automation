from pytest_bdd import when
from pytest_bdd.parsers import parse
from services.products import Products, ProductGet, ProductsSearch, ProductsCategory


# ===== WHEN STEPS (Products List) =====

@when("fetching all products", target_fixture="products_response")
def fetch_all_products(client) -> dict:
    """Action: Get all products with default pagination."""
    return client.get_request(Products.ENDPOINT, expected_status=200)


@when(parse("fetching products with limit {limit:d}, skip {skip:d} and sort by {field} {order}"), target_fixture="products_response")
def fetch_products_with_pagination_and_sort(client, limit, skip, field, order):
    """Action: Get products with custom pagination and sorting."""
    params = Products.get_params(limit=limit, skip=skip, sort_by=field, order=order)
    return client.get_request(Products.ENDPOINT, params=params, expected_status=200)


# ===== WHEN STEPS (Single Product) =====

@when(parse("fetching product at index {index:d} from list"), target_fixture="product_response")
def fetch_product_by_index_from_list(client, index, products_response) -> dict:
    """Action: Extract product ID at given index from list and fetch its details."""
    product_id = products_response["products"][index]["id"]
    return client.get_request(f"{ProductGet.ENDPOINT}{product_id}", expected_status=200)



@when(parse("fetching product with invalid ID {product_id:d}"), target_fixture="product_error_response")
def fetch_invalid_product(client, product_id) -> dict:
    """Action: Attempt to fetch product with invalid ID (negative test)."""
    return client.get_request(f"{ProductGet.ENDPOINT}{product_id}", expected_status=404)


# ===== WHEN STEPS (Search) =====

@when(parse('searching products with query {query}'), target_fixture="products_response")
def search_products(client, query) -> dict:
    """Action: Search products by query string."""
    params = ProductsSearch.get_params(query=query)
    return client.get_request(ProductsSearch.ENDPOINT, params=params, expected_status=200)


@when(parse("fetching product at index {index:d} from search results"), target_fixture="product_response")
def fetch_product_by_index_from_search(client, index, products_response) -> dict:
    """Action: Extract product ID at given index from search results and fetch its details."""
    product_id = products_response["products"][index]["id"]
    return client.get_request(f"{ProductGet.ENDPOINT}{product_id}", expected_status=200)

# ===== WHEN STEPS (Category) =====

@when(parse('fetching products in category {category}'), target_fixture="products_response")
def fetch_products_by_category(client, category) -> dict:
    """Action: Get products filtered by category."""
    return client.get_request(f"{ProductsCategory.ENDPOINT}/{category}", expected_status=200)