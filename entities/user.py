from API.api_manager import ApiManager

class User:
    def __init__(self, email: str, roles: list, api: ApiManager, password: str):
        self.email = email
        self.password = password
        self.roles = roles
        self.api = api

        @property
        def creds(self):
            return self.email, self.password
