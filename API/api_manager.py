from API.movies_api import MoviesAPI
from API.auth_api import AuthAPI
from API.user_api import UserApi
from constants import AUTH_BASE_URL, API_BASE_URL

class ApiManager:
    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url
        self.auth_api = AuthAPI(session, AUTH_BASE_URL)
        self.user_api = UserApi(session, AUTH_BASE_URL)
        self.movies_api = MoviesAPI(session, API_BASE_URL)

    def close_session(self):
        self.session.close()