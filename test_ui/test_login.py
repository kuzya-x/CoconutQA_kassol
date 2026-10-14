import allure
import pytest
from playwright.sync_api import expect


@allure.epic("Тестирование UI")
@allure.feature("Авторизация")
@pytest.mark.ui
class TestLogin:
    @allure.title("Успешная авторизация пользователя")
    def test_login_ui(self, login_page, page, common_user):
        user = common_user
        email = user.email
        password = user.password
        login_page.login(email, password)
        expect(page.get_by_text("Что-то пошло не так")).to_be_visible()
"""Страница после спешного логина выдаёт баннер 'Что-то пошло не так' после обновления выкидывает на главную уже с логином"""

    