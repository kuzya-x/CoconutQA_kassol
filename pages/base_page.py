
import allure
from constants import UI_BASE_URL
from pages.actions import PageAction

class BasePage(PageAction):
    def __init__(self, page):
        super().__init__(page)
        self.home_url = UI_BASE_URL
        self.all_movies_link = 'a[href="/movies"]'
        self.profile_button = 'button:text-is("Профиль")'

    @allure.step("Переход на 'Все фильмы' из шапки")
    def go_to_all_movies(self):
        self.click(self.all_movies_link)

    @allure.step("Проверить, что выполнен вход под {email}")
    def assert_logged_in_as(self, email: str):
        self.reload()
        self.wait_for_visible(self.profile_button)
        self.click(self.profile_button)
        self.assert_text_visible(email)