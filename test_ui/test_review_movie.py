import random
import allure
import pytest
from utils.movie_data_generator import MovieDataGenerator


@allure.epic("Тестирование UI")
@allure.feature("Отзывы")
@pytest.mark.ui
class TestReview:
    @allure.title("Публикация отзыва под фильмом")
    @allure.description("Вошедший пользователь оставляет отзыв под фильмом")
    @pytest.mark.smoke
    def test_leave_review(self, login_page, review_page, common_user, created_movie):
        rating = random.randint(1, 5)
        review_text = MovieDataGenerator.generate_review_text()

        with allure.step("Подготовка: вход и открытие страницы фильма"):
            login_page.login(common_user.email, common_user.password)
            login_page.assert_logged_in_as(common_user.email)
            review_page.open(created_movie)

        with allure.step("Действие: заполнить и отправить отзыв"):
            review_page.fill_review(review_text)
            review_page.select_rating(rating)
            review_page.assert_rating_selected(rating)
            review_page.submit_review()

        with allure.step("Проверка: отзыв опубликован"):
            review_page.assert_success_notification()
            review_page.assert_review_displayed(review_text)