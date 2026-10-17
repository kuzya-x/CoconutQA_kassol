from API.user_api import UserApi
import pytest
from models.base_models import RegisterUserResponse
from pydantic import ValidationError

@pytest.mark.smoke
class TestUser:

    def test_create_user(self, super_admin, creation_user_data):
        response = super_admin.api.user_api.create_user(creation_user_data)
        created_user = RegisterUserResponse(**response.json())

        assert created_user.email == creation_user_data.email
        assert created_user.fullName == creation_user_data.fullName
        assert created_user.roles == creation_user_data.roles
        assert created_user.verified is True

    def test_get_user_by_locator(self, super_admin, creation_user_data):
        created_user_response = super_admin.api.user_api.create_user(creation_user_data).json()
        created_user = RegisterUserResponse(**created_user_response)
        response_by_id = super_admin.api.user_api.get_user(created_user.id).json()
        response_by_id_reg = RegisterUserResponse(**response_by_id)
        response_by_email = super_admin.api.user_api.get_user(created_user.email).json()
        response_by_email_reg = RegisterUserResponse(**response_by_email)

        assert response_by_id_reg == response_by_email_reg, "Содержание ответов должно быть идентичным"
        assert created_user.id != '', "ID должен быть не пустым"
        assert created_user.email == creation_user_data.email
        assert created_user.fullName == creation_user_data.fullName
        assert created_user.roles == creation_user_data.roles
        assert created_user.verified is True
        assert created_user.banned is False


    @pytest.mark.slow
    def test_get_user_by_id_common_user(self, common_user):
        common_user.api.user_api.get_user(common_user.email, expected_status=403)


