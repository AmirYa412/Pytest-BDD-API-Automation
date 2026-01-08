"""Authentication step definitions - reusable across features."""

from pytest_bdd import given, when, parsers
from requests import Response
from helpers.auth import AuthLogin, AuthRefresh, AuthMe


# ===== GIVEN STEPS =====

@given(parsers.parse('user "{user_name}" is authenticated'), target_fixture="auth_response")
def authenticate_specific_user(client, user_name: str) -> str:
    """Authenticate specific user and set Bearer token in session."""
    user = client.users[user_name]
    payload = AuthLogin.get_payload(user["username"], user["password"])
    response = client.post_request(AuthLogin.ENDPOINT, json=payload, expected_status=200)

    token = response["accessToken"]
    client.session.headers.update({"Authorization": f"Bearer {token}"})
    return response


# ===== WHEN STEPS =====

@when(parsers.parse('user attempts to login with username "{username}" and password "{password}"'),
      target_fixture="auth_response")
def login_with_credentials(client, username: str, password: str) -> Response:
    """Attempt login with specific credentials."""
    payload = AuthLogin.get_payload(username, password)
    return client.post_request(AuthLogin.ENDPOINT, json=payload, expected_status=200)


@when("user attempts to login with missing password", target_fixture="auth_response")
def login_with_missing_password(client) -> Response:
    """Attempt login with missing password field."""
    user = client.users["Emily"]
    payload = AuthLogin.get_payload(username=user["username"])  # password=None
    return client.post_request(AuthLogin.ENDPOINT, json=payload, expected_status=200)


@when("user attempts to login with empty credentials", target_fixture="auth_response")
def login_with_empty_credentials(client) -> Response:
    """Attempt login with empty credential fields."""
    payload = AuthLogin.get_payload("", "")
    return client.post_request(AuthLogin.ENDPOINT, json=payload, expected_status=200)


@when("user refreshes authentication token", target_fixture="refresh_response")
def refresh_auth_token(client, auth_response) -> Response:
    """Attempt to refresh access token."""
    refresh_token = auth_response.json().get("refreshToken")
    payload = AuthRefresh.get_payload(refresh_token)
    return client.post_request(AuthRefresh.ENDPOINT, json=payload, expected_status=200)

