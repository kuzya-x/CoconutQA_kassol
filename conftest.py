import pytest
import requests
from utils.movie_data_generator import MovieDataGenerator
from constants import AUTH_BASE_URL, API_BASE_URL, LOGIN_ENDPOINT, HEADERS
from API.api_manager import ApiManager
from utils.user_data_generator import DataGenerator
from API.user_api import User
from resources.user_creds import SuperAdminCreds
from enums.roles import Roles
from models.base_models import TestUser
from sqlalchemy.orm import Session
from db_requester.db_client import get_db_session
from db_requester.db_helpers import DBHelper
from playwright.sync_api import Page
from pages.register_page import CinescopeRegisterPage
from pages.login_page import CinescopeLoginPage
from pages.review_page import CinescopeReviewPage


@pytest.fixture
def test_user() -> TestUser:
    random_password = DataGenerator.generate_random_password()

    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER]
    )
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
    assert response.status_code == 201, f"Ошибка авторизаци: {response.status_code}"

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
def creation_user_data(test_user: TestUser) -> TestUser:
    return test_user.model_copy(update={"verified": True, "banned": False})

@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.ADMIN_USERNAME,
        SuperAdminCreds.ADMIN_PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture
def common_user(user_session, super_admin, creation_user_data, db_helper):
    new_session = user_session()

    common_user = User(
        creation_user_data.email,
        creation_user_data.password,
        [Roles.USER.value],
        new_session)
    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)

    yield common_user

    user_in_db = db_helper.get_user_by_email(common_user.email)
    if user_in_db:
        db_helper.delete_user(user_in_db)


@pytest.fixture
def admin_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    admin_user = User(
        creation_user_data.email,
        creation_user_data.password,
        [Roles.ADMIN.value],
        new_session
    )
    super_admin.api.user_api.create_user(creation_user_data)
    admin_user.api.auth_api.authenticate(admin_user.creds)
    return admin_user

@pytest.fixture(scope="module")
def db_session() -> Session:
    """
    Фикстура, которая создает и возвращает сессию для работы с базой данных
    После завершения теста сессия автоматически закрывается
    """
    db_session = get_db_session()
    yield db_session
    db_session.close()

@pytest.fixture(scope="function")
def db_helper(db_session) -> DBHelper:
    """
    Фикстура для экземпляра хелпера
    """
    db_helper = DBHelper(db_session)
    return db_helper

@pytest.fixture(scope="function")
def created_test_user(db_helper):
    """
    Фикстура, которая создает тестового пользователя в БД
    и удаляет его после завершения теста
    """
    user = db_helper.create_test_user(DataGenerator.generate_user_data())
    yield user
    # Cleanup после теста
    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)

@pytest.fixture
def register_page(page: Page) -> CinescopeRegisterPage:
    register_page = CinescopeRegisterPage(page)
    register_page.open()
    return register_page

@pytest.fixture
def login_page(page: Page) -> CinescopeLoginPage:
    login_page = CinescopeLoginPage(page)
    login_page.open()
    return login_page

@pytest.fixture
def review_page(page: Page) -> CinescopeReviewPage:
    return CinescopeReviewPage(page)