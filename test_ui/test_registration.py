from utils.user_data_generator import DataGenerator
import allure
import pytest
from playwright.sync_api import expect

@allure.epic("Тестирование UI")
@allure.feature("Регистрация")
@pytest.mark.ui
class TestRegistration:
    @allure.title("Успешная регистрация нового пользователя")
    @pytest.mark.smoke
    def test_registration(self, register_page, page):
        email = DataGenerator.generate_random_email()
        register_page.register("Иван Иванов", email, "qwerty123Q")
        expect(page.get_by_text("Подтвердите свою почту")).to_be_visible()