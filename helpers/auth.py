"""Authentication endpoint helpers."""

from typing import Dict, Optional


class AuthLogin:
    """Helper for authentication login endpoint."""

    ENDPOINT = "/auth/login"

    @staticmethod
    def get_payload(username: str = None, password: str = None) -> Dict:
        """Build login request payload.

        Args:
            username: Username for authentication (optional)
            password: Password for authentication (optional)

        Returns:
            Login request body dictionary
        """
        payload = {
            "username": username,
            "password": password
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

    # Note: This endpoint doesn't require a request body (GET request)
    # Token is passed via Authorization header