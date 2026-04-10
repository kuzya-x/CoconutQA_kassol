import pytest
from API.api_manager import ApiManager
from utils.movie_data_generator import MovieDataGenerator


class TestMoviesAPI:

    def test_get_movies_list(self, api_manager):
        response = api_manager.movies_api.get_movies()
        assert response.status_code == 200, f"Ожидали код 200, получили:{response.status_code}"
        data = response.json()
        assert "movies" in data

    def test_create_movie(self, api_manager):
        movie_data = MovieDataGenerator.generate_movie_data()
        response = api_manager.movies_api.create_movie(movie_data)
        assert response.status_code == 201, f"Ожидали код 201, получили:{response.status_code}"
        movie_id = response.json()["id"]
        get_response = api_manager.movies_api.get_movie_by_id(movie_id)
        assert get_response.status_code == 200, f"Ожидали код 200, получили:{response.status_code}"
        api_manager.movies_api.delete_movie(movie_id)

    def test_get_movie_by_id(self, api_manager, created_movie):
        response = api_manager.movies_api.get_movie_by_id(created_movie)
        assert response.status_code == 200, f"Ожидали код 200, получили:{response.status_code}"
        assert response.json()["id"] == created_movie, f"id Созданого фильма не совпадает с полученым"

    def test_update_movie(self, api_manager, created_movie):
        update_data = {"name": MovieDataGenerator.generate_name()}
        response = api_manager.movies_api.update_movie(created_movie, update_data)
        assert response.status_code == 200, f"Ожидали код 200, получили:{response.status_code}"
        assert response.json()["name"] == update_data["name"], f"Название фильме не изменилось на {update_data['name']}"

    def test_delete_movie(self, api_manager):
        movie_data = MovieDataGenerator.generate_movie_data()
        response = api_manager.movies_api.create_movie(movie_data)
        assert response.status_code == 201, f"Ожидали код 201, получили:{response.status_code}"
        movie_id = response.json()["id"]
        delete_move = api_manager.movies_api.delete_movie(movie_id)
        assert delete_move.status_code == 200, f"Ожидали код 200, получили:{response.status_code}"
        get_response = api_manager.movies_api.get_movie_by_id(movie_id, expected_status=404)
        assert get_response.status_code == 404, f"Ожидали код 404, получили:{response.status_code}"

    def test_get_movie_by_invalid_id(self, api_manager):
        response = api_manager.movies_api.get_movie_by_id(movie_id=999999999, expected_status=404)
        assert response.status_code == 404, f"Ожидали код 404, получили:{response.status_code}"
        assert "message" in response.json()

    def test_create_movie_invalid_data(self, api_manager):
        response = api_manager.movies_api.create_movie(movie_data={}, expected_status=400)
        assert response.status_code == 400
        assert "message" in response.json()

    def test_delete_nonexistent_movie(self, api_manager):
        response = api_manager.movies_api.delete_movie(movie_id=999999, expected_status=404)
        assert response.status_code == 404

