from playwright.sync_api import Page
from urllib3.util import url
import random
from pages.base_page import BasePage

class CinescopeReviewPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url = f"{self.home_url}movies/77856"
        self.rating_value = 'button[role="combobox"]'
        self.review_input = '[data-qa-id="movie_review_input"]'
        self.rating_trigger = 'button[role="combobox"]:has([data-qa-id="movie_rating_select"])'
        self.rating_option = '[role="option"]'
        self.submit_button = '[data-qa-id="movie_review_submit_button"]'

    def select_rating(self, rating: int):
        rating = random.randint(1, 5)
        self.page.locator(self.rating_trigger).click()
        option = self.page.get_by_role("option", name=str(rating), exact=True)
        option.wait_for(state="visible")
        option.click()

    def fill_review(self, text: str):
        self.enter_text(self.review_input, text)

    def open(self):
        self.open_url(self.url)

    def submit_review(self):
        self.click(self.submit_button)

    def leave_review(self, text: str, rating: int):
        self.fill_review(text)
        self.select_rating(rating)
        self.submit_review()

