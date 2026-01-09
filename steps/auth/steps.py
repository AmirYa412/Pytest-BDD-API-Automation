from pytest_bdd import given, when
from pytest_bdd.parsers import parse
from services.auth import AuthLogin, AuthMe

# ===== GIVEN STEPS =====

@given(parse('user {user_name} is authenticated'), target_fixture="login_response")
def authenticate_specific_user(client, user_name: str) -> dict:
    """Setup step: Authenticate and return response."""
    user = client.users[user_name]
    payload = AuthLogin.get_payload(user["username"], user["password"])

    response = client.post_request(AuthLogin.ENDPOINT, json=payload, expected_status=200)
    token = response["accessToken"]
    client.session.headers.update({"Authorization": f"Bearer {token}"})
    return response

# ===== WHEN STEPS (Login) =====

@when(parse("{user_name} attempts to login with {password} password"), target_fixture="login_response")
def login_with_bad_password(client, user_name, password) -> dict:
    """Action: Login invalid. Still returns auth_response."""
    if password == "missing":
        payload = AuthLogin.get_payload(username=client.users[user_name]["username"])
    else:
        payload = AuthLogin.get_payload(username=client.users[user_name], password=password)
    return client.post_request(AuthLogin.ENDPOINT, json=payload, expected_status=400)

# ===== WHEN STEPS (Profile) =====

@when("fetching user profile", target_fixture="profile_response")
def fetch_own_profile(client) -> dict:
    """Action: Get Profile."""
    return client.get_request(AuthMe.ENDPOINT, expected_status=200)