import allure
import pytest
from playwright.sync_api import expect


@allure.epic("Тестирование UI")
@allure.feature("Авторизация")
@pytest.mark.ui
class TestLogin:
    @allure.title("Успешная авторизация пользователя")
    @allure.description("После входа и обновления страницы в профиле виден email пользователя")
    @pytest.mark.smoke
    def test_login_ui(self, login_page, common_user):
        login_page.login(common_user.email, common_user.password)
        login_page.assert_logged_in_as(common_user.email)
    