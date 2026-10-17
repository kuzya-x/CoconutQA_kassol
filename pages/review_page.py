import allure
from pages.base_page import BasePage

class CinescopeReviewPage(BasePage):
    success_notification = "Отзыв успешно создан"

    def __init__(self, page):
        super().__init__(page)
        self.url = f"{self.home_url}movies"
        self.review_input = '[data-qa-id="movie_review_input"]'
        self.rating_value = '[data-qa-id="movie_rating_select"]'
        self.rating_trigger = f'button[role="combobox"]:has({self.rating_value})'
        self.submit_button = '[data-qa-id="movie_review_submit_button"]'

    @allure.step("Выбрать оценку {rating}")
    def select_rating(self, rating: int):
        self.click(self.rating_trigger)
        self.select_list_option(str(rating))

    @allure.step("Написать текст отзыва")
    def fill_review(self, text: str):
        self.enter_text(self.review_input, text)

    @allure.step("Открыть страницу фильма с id {movie_id}")
    def open(self, movie_id: int):
        self.open_url(f"{self.url}/{movie_id}")
        self.wait_for_visible(self.review_input)

    @allure.step("Отправить отзыв")
    def submit_review(self):
        self.click(self.submit_button)

    @allure.step("Оставить отзыв с оценкой {rating}")
    def leave_review(self, text: str, rating: int):
        self.fill_review(text)
        self.select_rating(rating)
        self.submit_review()

    @allure.step("Проверить, что выбрана оценка {rating}")
    def assert_rating_selected(self, rating: int):
        self.assert_text(self.rating_value, str(rating))

    @allure.step("Проверить уведомление об успешной публикации")
    def assert_success_notification(self):
        self.assert_text_visible(self.success_notification)

    @allure.step("Проверить, что отзыв отображается на странице")
    def assert_review_displayed(self, text: str):
        self.assert_text_visible(text, exact=True)

