import pytest
import requests
from utils.movie_data_generator import MovieDataGenerator
from constants import AUTH_BASE_URL, API_BASE_URL, LOGIN_ENDPOINT, HEADERS
from API.api_manager import ApiManager
from utils.user_data_generator import DataGenerator
from API.user_api import User
from credentials import SuperAdminCreds
from enums.roles import Roles

@pytest.fixture(scope="function")
def test_user():
    """
    Генерация случайного пользователя для тестов.
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": [Roles.USER.value]
    }

@pytest.fixture()
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session, AUTH_BASE_URL)
        user_pool.append(user_session)
        return user_session
    yield _create_user_session

    for user in user_pool:
        user.close_session()

@pytest.fixture(scope="session")
def auth_session():
    session = requests.Session()
    login_data = {
        "email": SuperAdminCreds.ADMIN_USERNAME,
        "password": SuperAdminCreds.ADMIN_PASSWORD
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

@pytest.fixture(scope="function")
def creation_user_data(test_user):
    updated_data = test_user.copy()
    updated_data.update({
        "verified": True,
        "banned": False
    })
    return updated_data

@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.ADMIN_USERNAME,
        SuperAdminCreds.ADMIN_PASSWORD,
        "[SUPER_ADMIN]",
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        list(Roles.USER.value),
        new_session)
    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user


@pytest.fixture
def admin_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    admin_user = User(
        creation_user_data["email"],
        creation_user_data["password"],
        list(Roles.ADMIN.value),
        new_session
    )
    super_admin.api.user_api.create_user(creation_user_data)
    admin_user.api.auth_api.authenticate(admin_user.creds)
    return admin_user

