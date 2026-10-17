from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from enums.roles import Roles

EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

class TestUser(BaseModel):
    """Тело запроса на создание пользователя (POST /register и POST /user)."""

    email: str = Field(..., pattern=EMAIL_PATTERN, description="Email пользователя")
    fullName: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8, max_length=20)
    passwordRepeat: str = Field(..., min_length=8, max_length=20)
    roles: list[Roles] = [Roles.USER]
    verified: Optional[bool] = None
    banned: Optional[bool] = None

    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value: str, info) -> str:
        """passwordRepeat обязан совпадать с password."""
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("passwordRepeat не совпадает с password")
        return value

class RegisterUserResponse(BaseModel):
    """Ответ на POST /register и POST /user."""

    id: str
    email: str = Field(..., pattern=EMAIL_PATTERN)
    fullName: str = Field(..., min_length=1, max_length=100)
    verified: bool
    banned: bool
    roles: list[Roles]
    createdAt: datetime




class Location(str, Enum):
    MSK = "MSK"
    SPB = "SPB"


class Genre(BaseModel):
    name: str
    id: Optional[int] = None


class Movie(BaseModel):
    id: int
    name: str
    description: str
    genreId: int
    imageUrl: Optional[str] = None
    price: int
    rating: float = Field(..., ge=0, le=5)
    location: Location
    published: bool
    createdAt: datetime
    genre: Genre


class MoviesPage(BaseModel):
    movies: list[Movie]
    count: int
    page: int
    pageSize: int
    pageCount: int