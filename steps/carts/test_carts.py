from pytest_bdd import scenarios, then
from pytest_bdd.parsers import parse
from utilities.schema_validation import validate_schema
from services.carts import CartGet, CartUpdate, CartDelete

scenarios("../../features/carts.feature")


# ====== Schema validation steps ======

@then("cart schema should be valid")
def verify_cart_schema(cart_response):
    """Validate single cart response against schema."""
    validate_schema(cart_response, CartGet.SCHEMA)


@then("update cart schema should be valid")
def verify_update_cart_schema(update_cart_response):
    """Validate cart update response against schema."""
    validate_schema(update_cart_response, CartUpdate.SCHEMA)


@then("delete cart schema should be valid")
def verify_delete_cart_schema(delete_cart_response):
    """Validate cart delete response against schema."""
    validate_schema(delete_cart_response, CartDelete.SCHEMA)


# ====== Response content validations ======

@then("cart data is valid")
def verify_cart_data(cart_response):
    """Verify single cart data logic and business rules."""
    # IDs validations
    assert cart_response["id"] > 0, "Cart ID must be positive"
    assert cart_response["userId"] > 0, "User ID must be positive"

    # Products validation
    assert len(cart_response["products"]) > 0, "Cart must contain at least one product"
    assert cart_response["total"] > 0, "Cart total must be positive"
    assert cart_response["discountedTotal"] >= 0, "Discounted total cannot be negative"
    assert cart_response["totalProducts"] > 0, "Total products count must be positive"
    assert cart_response["totalQuantity"] > 0, "Total quantity must be positive"

    # Product items validation
    for product in cart_response["products"]:
        assert product["id"] > 0, "Product ID must be positive"
        assert len(product["title"]) > 0, "Product title cannot be empty"
        assert product["price"] > 0, "Product price must be positive"
        assert product["quantity"] > 0, "Product quantity must be positive"
        assert product["total"] > 0, "Product total must be positive"


@then("cart belongs to authenticated user")
def verify_cart_belongs_to_user(cart_response, login_response):
    """Verify cart belongs to the authenticated user."""
    expected_user_id = login_response["id"]
    actual_user_id = cart_response["userId"]
    assert actual_user_id == expected_user_id, f"Expected cart to belong to user {expected_user_id}, got {actual_user_id}"


@then(parse("cart contains product {product_id:d} with quantity {quantity:d}"))
def verify_cart_contains_product_with_quantity(update_cart_response, product_id, quantity):
    """Verify cart contains specific product with exact quantity."""
    products = update_cart_response["products"]

    # Find the product in cart
    product_found = False
    for product in products:
        if product["id"] == product_id:
            product_found = True
            actual_quantity = product["quantity"]
            assert actual_quantity == quantity, f"Product {product_id} has quantity {actual_quantity}, expected {quantity}"
            break

    assert product_found, f"Product {product_id} not found in cart"


@then("cart is marked as deleted")
def verify_cart_is_deleted(delete_cart_response):
    """Verify cart has deletion markers from DummyJSON API."""
    # Verify isDeleted field exists and is True
    assert "isDeleted" in delete_cart_response, "Cart response missing 'isDeleted' field"
    assert delete_cart_response["isDeleted"] is True, f"Expected isDeleted=True, got {delete_cart_response['isDeleted']}"

    # Verify deletedOn timestamp exists
    assert "deletedOn" in delete_cart_response, "Cart response missing 'deletedOn' field"
    assert len(delete_cart_response["deletedOn"]) > 0, "deletedOn timestamp is empty"
