from custom_requester.custom_requester import CustomRequester

class User:
    def __init__(self, email: str, password: str, roles: list, api):
        self.email = email
        self.password = password
        self.roles = roles
        self.api = api  # Сюда будем передавать экземпляр API Manager для запросов

    @property
    def creds(self):
        """Возвращает кортеж (email, password)"""
        return self.email, self.password

class UserApi(CustomRequester):
    def __init__(self, session, base_url):
        super().__init__(session=session, base_url=base_url)

    def get_user(self, user_locator, expected_status=200):
        return self.send_request("GET", f"user/{user_locator}", expected_status=expected_status)

    def create_user(self, user_data, expected_status=201):
        return self.send_request(
            method="POST",
            endpoint="user",
            data=user_data,
            expected_status=expected_status
        )