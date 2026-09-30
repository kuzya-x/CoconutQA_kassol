
import pytest

from models.base_models import Movie, MoviesPage
from utils.movie_data_generator import MovieDataGenerator
import random
import allure

@pytest.mark.api
@allure.epic("Cinescope API")
@allure.feature("Movies")
class TestMoviesPositive:


    @pytest.mark.smoke
    @allure.title("Проверка выдачи списка фильмов")
    def test_get_movies_list(self, api_manager):
        with allure.step("Запрос списка фильмов"):
            response = api_manager.movies_api.get_movies()
            assert response.status_code == 200
        with allure.step("Проверка структуры ответа"):
            movies_page = MoviesPage(**response.json())
            assert isinstance(movies_page.movies, list)

    @allure.title("Проверка создания фильма")
    @pytest.mark.smoke
    def test_create_movie(self, api_manager):
        with allure.step("Генерация данных и создание фильма"):
            movie_data = MovieDataGenerator.generate_movie_data()
            response = api_manager.movies_api.create_movie(movie_data)
            assert response.status_code == 201
        with allure.step("Проверка на наличие созданного фильма"):
            movie_id = response.json()["id"]
            get_response = api_manager.movies_api.get_movie_by_id(movie_id)
            assert get_response.status_code == 200
        with allure.step("Проверка структуры и данных созданного фильма"):
            created_movie = Movie(**get_response.json())
            assert created_movie.name == movie_data["name"], f"Ожидаемое название фильма: {movie_data['name']}, фактическое: {created_movie.name}"
            assert created_movie.price == movie_data["price"], f"Ожидаемая цена билета: {movie_data['price']}, фактическая: {created_movie.price}"
            assert created_movie.location == movie_data["location"], f"Ожидаемая локация фильма: {movie_data['location']}, фактическая: {created_movie.location}"
            assert created_movie.description == movie_data["description"], f"Ожидаемое описание фильма: {movie_data['description']}, фактическое: {created_movie.description}"
            assert created_movie.genreId == movie_data["genreId"], f"Ожидаемый жанр id: {movie_data['genreId']}, фактический: {created_movie.genreId}"
            assert created_movie.imageUrl == movie_data["imageUrl"], f"Ожидаемый url изображения: {movie_data['imageUrl']}, фактический: {created_movie.imageUrl}"
            assert created_movie.published == movie_data["published"], f"Ожидаемое состояние публикации: {movie_data['published']}, фактическое: {created_movie.published}"
        with allure.step("Удаление созданного фильма"):
            api_manager.movies_api.delete_movie(movie_id)

    @allure.title("Проверка поиска фильма по id")
    @pytest.mark.regression
    def test_get_movie_by_id(self, api_manager, created_movie):
        with allure.step("Поиск фильма по id"):
            response = api_manager.movies_api.get_movie_by_id(created_movie)
            assert response.status_code == 200
            movie_by_id = Movie(**response.json())
            assert movie_by_id.id == created_movie, f"id Созданого фильма не совпадает с полученым"

    @allure.title("Проверка обновления данных фильма")
    @pytest.mark.regression
    def test_update_movie(self, api_manager, created_movie):
        with allure.step("Генерации name фильма"):
            update_data = {"name": MovieDataGenerator.generate_name()}
        with allure.step("Обновлене данных фильма"):
            response = api_manager.movies_api.update_movie(created_movie, update_data)
            assert response.status_code == 200
            movie_update = Movie(**response.json())
            assert movie_update.name == update_data["name"], f"Название фильме не изменилось на {update_data['name']}"

    @allure.title("Проверка удаления фильма")
    @pytest.mark.regression
    def test_delete_movie(self, api_manager):
        with allure.step("Генерации данных фильма"):
            movie_data = MovieDataGenerator.generate_movie_data()
        with allure.step("Создание фильма"):
            response = api_manager.movies_api.create_movie(movie_data)
            assert response.status_code == 201
        with allure.step("Удаление фильма по id"):
            movie_delete = Movie(**response.json())
            delete_move = api_manager.movies_api.delete_movie(movie_delete.id)
            assert delete_move.status_code == 200
        with allure.step("Удостоверяемся в удаление фильма"):
            get_response = api_manager.movies_api.get_movie_by_id(movie_delete.id, expected_status=404)
            assert get_response.status_code == 404

    @allure.title("Проверка выдачи фильмов по фильтру локации")
    @pytest.mark.regression
    def test_get_movies_with_filter_location(self, api_manager):
        with allure.step("Выбор локации"):
            locations = ["SPB", "MSK"]
            selected_location = random.choice(locations)
        with allure.step(f"Поиск фильмов по локации {selected_location}"):
            response = api_manager.movies_api.get_movies(params={"locations" : selected_location})
            movies_page = MoviesPage(**response.json())
            assert response.status_code == 200
            assert isinstance(movies_page.movies, list), f"{movies_page.movies} не является списком"
        with allure.step(f"Проверка все ли полученные фильмы с локацией {selected_location}"):
            for movie in movies_page.movies:
                assert movie.location == selected_location, f"Локация {movie.location} не является {selected_location}"

    @allure.title(f"Проверка Поиска фильма по параметрам")
    @pytest.mark.parametrize("params, check_field, expected, check_type", [
        ({"price_from": 1, "price_to": 1000}, "price", (1, 1000), "range"),
        ({"locations": "SPB"}, "location", "SPB", "equal"),
        ({"genreId": 1}, "genreId", 1, "equal")
    ])
    def test_get_movies_parametrize_filter(self, api_manager, params, check_field, expected, check_type):
        with allure.step(f"Поиск фильмов по параметрам {params}"):
            response = api_manager.movies_api.get_movies(params=params)
            assert response.status_code == 200
            movies_params = MoviesPage(**response.json())
        with allure.step(f"Проверка фильмов на соответствие фильтров"):
            for movie in movies_params.movies:
                if check_type == "equal":
                    assert getattr(movie, check_field) == expected
                elif check_type == "range":
                    min_val, max_val = expected
                    assert min_val <= getattr(movie, check_field) <= max_val

    @allure.title("Проверка удаление фильма через Супер Админа")
    @pytest.mark.regression
    @pytest.mark.slow
    def test_delete_movie_roles(self, api_manager, super_admin):
        movie_data = MovieDataGenerator.generate_movie_data()
        with allure.step("Создание фильма"):
            response = super_admin.api.movies_api.create_movie(movie_data)
            movie_roles = Movie(**response.json())
            assert movie_roles.name == movie_data["name"], f"Ожидаемое название фильма: {movie_data['name']}, фактическое: {movie_roles.name}"
            assert movie_roles.price == movie_data["price"], f"Ожидаемая цена билета: {movie_data['price']}, фактическая: {movie_roles.price}"
        with allure.step("Удаление фильма"):
            super_admin.api.movies_api.delete_movie(movie_roles.id)
            get_response = super_admin.api.movies_api.get_movie_by_id(movie_roles.id, expected_status=404)
            assert get_response.status_code == 404

    @allure.tag("BD")
    @allure.title("Проверка на создание фильма в Базе данных")
    @pytest.mark.db
    def test_check_movie_to_bd(self, api_manager, db_helper):
        with allure.step("Удостоверяемся в отсутствие сегенерированного name в Базе данных"):
            movie_data = MovieDataGenerator.generate_movie_data()
            assert db_helper.get_movie_by_name(movie_data["name"]) is None
        with allure.step("Создание фильма"):
            response = api_manager.movies_api.create_movie(movie_data)
            movie_check = Movie(**response.json())
            movie_in_db = db_helper.get_movie_by_id(movie_check.id)
        with allure.step("Проверка на наличие фильма в БД"):
            assert movie_in_db is not None
            assert movie_in_db.name == movie_data["name"]
        with allure.step("Удаление фильма из БД"):
            api_manager.movies_api.delete_movie(movie_check.id)
            assert db_helper.get_movie_by_id(movie_check.id) is None


@allure.feature("Movies")
@allure.tag("negative")
@pytest.mark.api
@pytest.mark.negative
class TestMoviesErrors:

    @allure.title("Проверка получение фильма по невалидному id")
    @pytest.mark.regression
    def test_get_movie_by_invalid_id(self, api_manager):
        response = api_manager.movies_api.get_movie_by_id(movie_id=999999999, expected_status=404)
        assert response.status_code == 404
        assert "message" in response.json()

    @allure.title("Проверка создания фильма с пустыми данными")
    @pytest.mark.regression
    def test_create_movie_invalid_data(self, api_manager):
        response = api_manager.movies_api.create_movie(movie_data={}, expected_status=400)
        assert response.status_code == 400
        assert "message" in response.json()

    @allure.title("Проверка удаления несуществующего фильма")
    @pytest.mark.regression
    def test_delete_nonexistent_movie(self, api_manager):
        response = api_manager.movies_api.delete_movie(movie_id=999999, expected_status=404)
        assert response.status_code == 404

    @allure.title("Проверка создание фильма без необходимых прав")
    @pytest.mark.slow
    def test_create_movie_roles_user(self, common_user):
        movie_data = MovieDataGenerator.generate_movie_data()
        common_user.api.movies_api.create_movie(movie_data, expected_status=403)





