from http.client import responses

import pytest
from requests.utils import get_unicode_from_response
from credentials import SuperAdminCreds
from API.api_manager import ApiManager
from conftest import common_user, created_movie
from utils.movie_data_generator import MovieDataGenerator
import random
from constants import API_BASE_URL

class TestMoviesPositive:

    @pytest.makr.slow
    def test_get_movies_list(self, api_manager):
        response = api_manager.movies_api.get_movies()
        assert response.status_code == 200
        data = response.json()
        assert "movies" in data, f"отсутствует movies в ответе"
        assert isinstance(data["movies"], list), f"{data['movies']} не является списком"
        assert "count" in data, f"отсутствует count в ответе"
        assert "page" in data, f"отсутствует page в ответе"
        assert "pageSize" in data, f"отсутствует pageSize в ответе"
        assert "pageCount" in data, f"отсутствует pageCount в ответе"

    def test_create_movie(self, api_manager):
        movie_data = MovieDataGenerator.generate_movie_data()
        response = api_manager.movies_api.create_movie(movie_data)
        assert response.status_code == 201
        movie_id = response.json()["id"]
        get_response = api_manager.movies_api.get_movie_by_id(movie_id)
        assert get_response.status_code == 200
        created_movie = get_response.json()
        assert created_movie["name"] == movie_data["name"], f"Ожидаемое название фильма: {movie_data['name']}, фактическое: {created_movie['name']}"
        assert created_movie["price"] == movie_data["price"], f"Ожидаемая цена билета: {movie_data['price']}, фактическая: {created_movie['price']}"
        assert created_movie["location"] == movie_data["location"], f"Ожидаемая локация фильма: {movie_data['location']}, фактическая: {created_movie['location']}"
        assert created_movie["description"] == movie_data["description"], f"Ожидаемое описание фильма: {movie_data['description']}, фактическое: {created_movie['description']}"
        assert created_movie["genreId"] == movie_data["genreId"], f"Ожидаемый жанр id: {movie_data['genreId']}, фактический: {created_movie['genreId']}"
        assert created_movie["imageUrl"] == movie_data["imageUrl"], f"Ожидаемый url изображения: {movie_data['imageUrl']}, фактический: {created_movie['imageUrl']}"
        assert created_movie["published"] == movie_data["published"], f"Ожидаемое состояние публикации: {movie_data['published']}, фактическое: {created_movie['published']}"

        api_manager.movies_api.delete_movie(movie_id)


    def test_get_movie_by_id(self, api_manager, created_movie):
        response = api_manager.movies_api.get_movie_by_id(created_movie)
        assert response.status_code == 200
        assert response.json()["id"] == created_movie, f"id Созданого фильма не совпадает с полученым"

    def test_update_movie(self, api_manager, created_movie):
        update_data = {"name": MovieDataGenerator.generate_name()}
        response = api_manager.movies_api.update_movie(created_movie, update_data)
        assert response.status_code == 200
        assert response.json()["name"] == update_data["name"], f"Название фильме не изменилось на {update_data['name']}"

    def test_delete_movie(self, api_manager):
        movie_data = MovieDataGenerator.generate_movie_data()
        response = api_manager.movies_api.create_movie(movie_data)
        assert response.status_code == 201
        movie_id = response.json()["id"]
        delete_move = api_manager.movies_api.delete_movie(movie_id)
        assert delete_move.status_code == 200
        get_response = api_manager.movies_api.get_movie_by_id(movie_id, expected_status=404)
        assert get_response.status_code == 404

    def test_get_movies_with_filter_location(self, api_manager):
        locations = ["SPB", "MSK"]
        selected_location = random.choice(locations)
        response = api_manager.movies_api.get_movies(params={"locations" : selected_location})
        data = response.json()
        assert response.status_code == 200
        assert isinstance(data["movies"], list), f"{data['movies']} не является списком"
        for movie in data["movies"]:
            assert movie["location"] == selected_location, f"Локация {movie['location']} не является {selected_location}"


    @pytest.mark.parametrize("params, check_field, expected, check_type", [
        ({"price_from": 1, "price_to": 1000}, "price", (1, 1000), "range"),
        ({"locations": "SPB"}, "location", "SPB", "equal"),
        ({"genreId": 1}, "genreId", 1, "equal")
    ])
    def test_get_movies_parametrize_filter(self, api_manager, params, check_field, expected, check_type):
        response = api_manager.movies_api.get_movies(params=params)
        assert response.status_code == 200

        for movie in response.json()["movies"]:
            if check_type == "equal":
                assert movie[check_field] == expected
            elif check_type == "range":
                min_val, max_val = expected
                assert min_val <= movie[check_field] <= max_val

    @pytest.makr.slow
    def test_delete_movie_roles(self, api_manager, super_admin):
        movie_data = MovieDataGenerator.generate_movie_data()
        response = super_admin.api.movies_api.create_movie(movie_data)
        movie_id = response.json()["id"]
        created_movies = response.json()
        assert created_movies["name"] == movie_data["name"], f"Ожидаемое название фильма: {movie_data['name']}, фактическое: {created_movies['name']}"
        assert created_movies["price"] == movie_data["price"], f"Ожидаемая цена билета: {movie_data['price']}, фактическая: {created_movies['price']}"

        delete_movie = super_admin.api.movies_api.delete_movie(movie_id)
        get_response = super_admin.api.movies_api.get_movie_by_id(movie_id, expected_status=404)
        assert get_response.status_code == 404




class TestMoviesErrors:

    def test_get_movie_by_invalid_id(self, api_manager):
        response = api_manager.movies_api.get_movie_by_id(movie_id=999999999, expected_status=404)
        assert response.status_code == 404
        assert "message" in response.json()

    def test_create_movie_invalid_data(self, api_manager):
        response = api_manager.movies_api.create_movie(movie_data={}, expected_status=400)
        assert response.status_code == 400
        assert "message" in response.json()

    def test_delete_nonexistent_movie(self, api_manager):
        response = api_manager.movies_api.delete_movie(movie_id=999999, expected_status=404)
        assert response.status_code == 404

    @pytest.makr.slow
    def test_create_movie_roles_user(self, common_user):
        movie_data = MovieDataGenerator.generate_movie_data()
        common_user.api.movies_api.create_movie(movie_data, expected_status=403)