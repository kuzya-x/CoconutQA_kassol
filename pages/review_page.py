from playwright.sync_api import Page, expect
from urllib3.util import url
import random
from pages.base_page import BasePage

class CinescopeReviewPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url = f"{self.home_url}movies"
        self.rating_value = 'button[role="combobox"]'
        self.review_input = '[data-qa-id="movie_review_input"]'
        self.rating_trigger = 'button[role="combobox"]:has([data-qa-id="movie_rating_select"])'
        self.rating_option = '[role="option"]'
        self.submit_button = '[data-qa-id="movie_review_submit_button"]'

    def select_rating(self, rating: int):
        trigger = self.page.locator(self.rating_trigger)
        trigger.click()

        option = (self.page.get_by_role("listbox").get_by_role("option", name=str(rating), exact=True))
        expect(option).to_be_visible()
        option.click()
        expect(trigger).to_contain_text(str(rating))

    def fill_review(self, text: str):
        self.enter_text(self.review_input, text)

    def open(self, movie_id: int):
        self.open_url(f"{self.url}/{movie_id}")

    def submit_review(self):
        self.click(self.submit_button)

    def leave_review(self, text: str, rating: int):
        self.fill_review(text)
        self.select_rating(rating)
        self.submit_review()

