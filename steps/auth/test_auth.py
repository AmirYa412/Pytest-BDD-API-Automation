from pytest_bdd import scenarios, then, parsers
from utilities.schema_validation import validate_schema
from services.auth import AuthLogin, AuthMe

scenarios("../../features/auth.feature")


# ====== Schema validations steps ======


@then("login schema should be valid")
def verify_login_schema(login_response):
    """Explicitly validate the login response against the AuthLogin schema."""
    validate_schema(login_response, AuthLogin.SCHEMA)


@then("user profile schema should be valid")
def verify_login_schema(profile_response):
    """Explicitly validate the login response against the AuthLogin schema."""
    validate_schema(profile_response, AuthMe.SCHEMA)


# ====== Response content validations ======

@then("login data is valid")
def verify_login_data(login_response):
    """
    Verifies the LOGIC of the login response (Lengths, Formats).
    Types are already guaranteed by schema validation.
    """
    # Token Logic (Schema ensured they are strings, we ensure they have content)
    assert len(login_response["accessToken"]) > 20, "Access Token is suspiciously short"
    assert len(login_response["refreshToken"]) > 20, "Refresh Token is suspiciously short"

    # ID Logic (Schema ensured int, we ensure positive)
    assert login_response["id"] > 0, f"Invalid User ID: {login_response['id']}"

    # string Content Logic (Schema ensured string, we ensure non-empty)
    critical_fields = ["username", "firstName", "lastName", "email"]
    for field in critical_fields:
        assert len(login_response[field]) > 0, f"Field '{field}' is empty"

    # Format Logic
    assert "@" in login_response["email"], "Email format invalid"
    assert login_response["image"].startswith("http"), "Image URL must be absolute"


@then("login error schema should be valid")
def verify_login_error_400_schema(login_response):
    """Validates that the error response matches the expected JSON structure."""
    validate_schema(login_response, AuthLogin.ERROR_400_SCHEMA)


@then("user profile data is valid")
def verify_profile_data(profile_response, login_response):
    """Verifies profile data logic and consistency with the logged-in user."""
    # Cross-Check Identity (The "Me" endpoint must match the "Login" user)
    assert profile_response["id"] == login_response["id"], \
        f"Login ID: {login_response['id']} vs Profile ID: {profile_response['id']}"

    assert len(profile_response["username"]) > 0
    assert profile_response["username"] == login_response["username"], "Username mismatch between Login and Profile"
    assert len(profile_response["email"]) > 0
    assert profile_response["email"] == login_response["email"], "Email mismatch between Login and Profile"

    # Logic: Address validation
    address = profile_response["address"]
    assert len(address["city"]) > 0, "City is missing in address"
    assert address["coordinates"]["lat"] > 0, "Latitude is missing"  # Schema checks type, we check content

    # Bank validation
    assert len(profile_response["bank"]["iban"]) > 10, "IBAN is too short"

    # Role validation (Example of domain-specific logic)
    valid_roles = ["admin", "user", "moderator"]
    assert profile_response["role"] in valid_roles, f"Unknown role: {profile_response['role']}"


@then(parsers.parse('login error message should be {expected_message}'))
def verify_login_error_message(login_response, expected_message):
    """Verifies the specific text of the error message."""
    actual_message = login_response.get("message", "")
    assert actual_message == expected_message, f"Message mismatch! Expected: '{expected_message}', Got: '{actual_message}'"