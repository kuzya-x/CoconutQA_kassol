
from playwright.sync_api import Page
from pages.base_page import BasePage
import time
import allure

class CinescopeLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}login"


        self.email_input = '[data-qa-id="login_email_input"]'
        self.password_input = '[data-qa-id="login_password_input"]'
        self.submit_button = '[data-qa-id="login_submit_button"]'

    @allure.step("Открыть страницу входа")
    def open(self):
        self.open_url(self.url)
        self.wait_for_visible(self.email_input)

    @allure.step("Войти под пользователем {email}")
    def login(self, email: str, password: str):
        self.enter_text(self.email_input, email)
        self.enter_text(self.password_input, password)
        self.click(self.submit_button)
        time.sleep(3)