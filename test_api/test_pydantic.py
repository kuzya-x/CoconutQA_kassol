import logging
from pydantic import BaseModel, ValidationError
import pytest
from models.base_models import TestUser

logger = logging.getLogger(__name__)

class User(BaseModel):      # наследуемся от BaseModel - это включает всю механику Pydantic
    name: str               # имя должно быть строкой
    age: int                # возраст должен быть целым числом
    adult: bool             # совершеннолетие должно быть булевым значением

def get_user():
    return {
        "name": "Alice",
        "age": 25,
        "adult": "true"     # обратите внимание: строка, а не True
    }

def test_user_data():
    user = User(**get_user())       # распаковываем dict в именованные аргументы
    assert user.name == "Alice"
    logger.info(f"{user.name=} {user.age=} {user.adult=}")


def test_user_model_rejects_invalid_email():
    with pytest.raises(ValidationError):
        TestUser(email="не-почта", fullName="Иван", password="12345678",
                 passwordRepeat="12345678")