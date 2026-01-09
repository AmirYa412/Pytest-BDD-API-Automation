"""Authentication endpoint helpers."""

from typing import Dict, Optional


class AuthLogin:
    """Helper for authentication login endpoint."""

    ENDPOINT = "/auth/login"
    SCHEMA = {
        "type": "object",
        "properties": {
            "accessToken": {"type": "string"},
            "refreshToken": {"type": "string"},
            "id": {"type": "integer"},
            "username": {"type": "string"},
            "email": {"type": "string", "format": "email"},
            "firstName": {"type": "string"},
            "lastName": {"type": "string"},
            "gender": {"type": "string"},
            "image": {"type": "string"}
        },
        "required": ["accessToken", "refreshToken", "id", "username", "email"]
    }
    ERROR_400_SCHEMA = {
        "type": "object",
        "properties": {
            "message": {"type": "string"}
        },
        "required": ["message"]
    }

    @staticmethod
    def get_payload(username: str = None, password: str = None, expires_in_minutes: int = 30) -> Dict:
        """Build login request payload.

        Args:
            username: Username for authentication (optional)
            password: Password for authentication (optional)

        Returns:
            Login request body dictionary
            :param username:
            :param password:
            :param expires_in_minutes:
        """
        payload = {
            "username": username,
            "password": password,
            "expiresInMins": expires_in_minutes
        }
        return payload


class AuthRefresh:
    """Helper for token refresh endpoint."""

    ENDPOINT = "/auth/refresh"

    @staticmethod
    def get_payload(refresh_token: str, expires_in_mins: int = 30) -> Dict:
        """Build token refresh request payload.

        Args:
            refresh_token: Refresh token from previous login
            expires_in_mins: Token expiration time in minutes (default: 30)

        Returns:
            Token refresh request body dictionary
        """
        return {
            "refreshToken": refresh_token,
            "expiresInMins": expires_in_mins
        }


class AuthMe:
    """Helper for authenticated user profile endpoint."""

    ENDPOINT = "/auth/me"
    SCHEMA = {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "username": {"type": "string"},
            "email": {"type": "string", "format": "email"},
            "firstName": {"type": "string"},
            "lastName": {"type": "string"},
            "image": {"type": "string"}
        },
        "required": ["id", "username", "email"]
    }
    # Note: This endpoint doesn't require a request body (GET request)
    # Token is passed via Authorization header