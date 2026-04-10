from API.movies_api import MoviesAPI
from API.auth_api import AuthAPI
from API.user_api import UserAPI

class ApiManager:
    def __init__(self, session, base_url):
        self.session = session
        self.auth_api = AuthAPI(session, base_url)
        self.user_api = UserAPI(session, base_url)
        self.movies_api = MoviesAPI(session, base_url)