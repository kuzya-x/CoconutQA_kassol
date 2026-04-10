import pytest
import requests
from utils.movie_data_generator import MovieDataGenerator
from constants import AUTH_BASE_URL, API_BASE_URL, LOGIN_ENDPOINT, HEADERS
from credentials import ADMIN_USERNAME, ADMIN_PASSWORD
from API.api_manager import ApiManager

@pytest.fixture(scope="session")
def auth_session():
    session = requests.Session()
    login_data = {
        "email": ADMIN_USERNAME,
        "password": ADMIN_PASSWORD
    }
    login_url = f"{AUTH_BASE_URL}{LOGIN_ENDPOINT}"
    response = session.post(login_url, json=login_data, headers=HEADERS)
    assert response.status_code == 200, f"Ошибка авторизаци: {response.status_code}"

    token = response.json().get("accessToken")
    assert token is not None, "Токен не получен"

    session.headers.update({"Authorization": f"Bearer {token}"})
    return session

@pytest.fixture(scope="session")
def api_manager(auth_session):
    return ApiManager(auth_session, API_BASE_URL)

@pytest.fixture(scope="function")
def created_movie(api_manager):
    movie_data = MovieDataGenerator.generate_movie_data()
    response = api_manager.movies_api.create_movie(movie_data)
    movie_id = response.json()["id"]

    yield movie_id

    api_manager.movies_api.delete_movie(movie_id)


