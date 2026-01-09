from pytest_bdd import when
from pytest_bdd.parsers import parse
from services.carts import Carts, CartGet, CartAdd, CartUpdate, CartDelete


# ===== WHEN STEPS (Carts List) =====

@when("fetching all carts", target_fixture="carts_response")
def fetch_all_carts(client):
    """Action: Get all carts with default pagination."""
    return client.get_request(Carts.ENDPOINT, expected_status=200)


# ===== WHEN STEPS (Single Cart) =====

@when(parse("fetching cart at index {index:d} from carts list"), target_fixture="cart_response")
def fetch_cart_by_index_from_carts(client, index, carts_response):
    """Action: Extract cart ID at given index from carts list and fetch its details."""
    cart_id = carts_response["carts"][index]["id"]
    return client.get_request(f"{CartGet.ENDPOINT}{cart_id}", expected_status=200)


# ===== WHEN STEPS (Create Cart) =====

@when(parse("creating cart with product at index {index:d} and quantity {quantity:d}"), target_fixture="cart_response")
def create_cart_with_product_from_list(client, index, quantity, login_response, products_response):
    """Action: Create cart for authenticated user using product ID from products list."""
    user_id = login_response["id"]
    product_id = products_response["products"][index]["id"]
    products = [{"id": product_id, "quantity": quantity}]
    payload = CartAdd.get_payload(user_id=user_id, products=products)
    return client.post_request(CartAdd.ENDPOINT, json=payload, expected_status=201)


# ===== WHEN STEPS (Update Cart) =====

@when(parse("updating cart at index {index:d} with product {product_id:d} and quantity {quantity:d}"), target_fixture="update_cart_response")
def update_cart_from_list(client, index, product_id, quantity, carts_response):
    """Action: Extract cart ID from carts list and update it."""
    cart_id = carts_response["carts"][index]["id"]
    products = [{"id": product_id, "quantity": quantity}]
    payload = CartUpdate.get_payload(products=products)
    return client.put_request(f"{CartUpdate.ENDPOINT}/{cart_id}", json=payload, expected_status=200)


# ===== WHEN STEPS (Delete Cart) =====

@when(parse("deleting cart at index {index:d}"), target_fixture="delete_cart_response")
def delete_cart_from_list(client, index, carts_response):
    """Action: Extract cart ID from carts list and delete it."""
    cart_id = carts_response["carts"][index]["id"]
    return client.delete_request(f"{CartDelete.ENDPOINT}/{cart_id}", expected_status=200)
