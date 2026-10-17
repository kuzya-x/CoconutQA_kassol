
from pages.base_page import BasePage
import allure

class CinescopeRegisterPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url = f"{self.home_url}register"

        self.full_name_input = '[data-qa-id="register_full_name_input"]'
        self.email_input = '[data-qa-id="register_email_input"]'
        self.password_input = '[data-qa-id="register_password_input"]'
        self.repeat_password_input = '[data-qa-id="register_password_repeat_input"]'
        self.submit_button = '[data-qa-id="register_submit_button"]'

    @allure.step("Открыть страницу регистрации")
    def open(self):
        self.open_url(self.url)
        self.wait_for_visible(self.full_name_input)

    @allure.step("Зарегистрировать пользователя {email}")
    def register(self, full_name: str, email: str, password: str):
        self.enter_text(self.full_name_input, full_name)
        self.enter_text(self.email_input, email)
        self.enter_text(self.password_input, password)
        self.enter_text(self.repeat_password_input, password)
        self.click(self.submit_button)