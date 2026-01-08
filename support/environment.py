from support.users import CI_USERS, PRODUCTION_USERS


class Environment:
    """Configuration for test environment and API endpoints.

    Manages base URL, headers, API version, and test user credentials
    for different testing environments.
    """
    API_DOMAIN = "dummyjson.com"


    def __init__(self, env_prefix: str):
        self.env_prefix = env_prefix
        self.protocol = "https://"
        self.is_ci = self.get_environment_type()
        self.domain = self.get_domain()
        self.base_url = f"{self.protocol}{self.domain}"
        self.headers = self.get_environment_headers()
        self.users = self.get_automation_users()

    @staticmethod
    def get_environment_headers():
        headers = {
            "User-Agent": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image",
            "Content-type": "application/json; charset=UTF-8"
        }
        return headers

    def get_environment_type(self):
        """Determine if environment is CI/QA based on prefix."""
        return self.env_prefix in ("ci", "qa")

    def get_domain(self):
        """Get domain based on environment type(ci or prod)"""
        if self.is_ci:
            return f"{self.env_prefix}.{self.API_DOMAIN}"
        return self.API_DOMAIN

    def get_automation_users(self):
        """Get test user credentials based on environment type.

         Validates that all users have passwords configured.
         """
        users = CI_USERS if self.is_ci else PRODUCTION_USERS
        for user in users:
            if not users[user]["password"]:
                raise EnvironmentError(f"Missing password for user {user}")
        return users




