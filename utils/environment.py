class TestEnvironment:
    def __init__(self, env_prefix):
        self.env_prefix = env_prefix
        self.protocol = "https://"
        self.domain = f"{self.env_prefix}.typicode.com"
        self.headers = self.get_environment_headers()

    def get_environment_headers(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image",
            "Content-type": "application/json; charset=UTF-8",
            "Referer": f"https://{self.env_prefix}.typicode.com"
        }
        return headers
