import random
import time
import allure
import pytest
from playwright.sync_api import expect


@allure.epic("Тестирование UI")
@allure.feature("Отзывы")
@pytest.mark.ui
class TestReview:
    @allure.title("Публикация отзыва под фильмом")
    def test_leave_review(self, login_page, review_page, page, common_user, created_movie):
        rating = random.randint(1, 5)
        review_text = f"Отличный фильм {random.randint(1, 999999)}"
        allure.dynamic.title(f"Публикация отзыва с оценкой")

        login_page.login(common_user.email, common_user.password)
        expect(page.get_by_text("Что-то пошло не так")).to_be_visible()
        review_page.open(created_movie)
        review_page.fill_review(review_text)
        review_page.select_rating(rating)
        expect(page.locator(review_page.rating_value)).to_have_text(str(rating))

        review_page.submit_review()
        expect(page.get_by_text("Отзыв успешно создан")).to_be_visible()
        expect(page.get_by_text(review_text, exact=True)).to_be_visible()