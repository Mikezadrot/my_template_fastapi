from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime

CURRENT_YEAR = datetime.now().year

class AuthorBase(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("Author name cannot be empty or whitespace only")
        return v

class AuthorCreate(AuthorBase):
    pass

class AuthorRead(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class GenreBase(BaseModel):
    name: str

class GenreCreate(GenreBase):
    pass

class GenreRead(GenreBase):
    id: int

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    published_year: int
    # genre_names: List[str]

    @field_validator("title")
    @classmethod
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("Book title name cannot be empty or whitespace only")
        return v

    @field_validator("published_year")
    @classmethod
    def validate_year(cls, v):
        if not (1800 <= v <= CURRENT_YEAR):
            raise ValueError("Year must be between 1800 and current year")
        return v

class BookCreate(BookBase):
    author_id: int
    genre_names: List[str]


class BookRead(BookBase):
    id: int
    author: AuthorRead
    genres: List[GenreRead]

    class Config:
        orm_mode = True

class BookUpdate(BaseModel):
    title: Optional[str] = None
    published_year: Optional[int] = None
    genre_names: Optional[List[str]] = None
    author_id: Optional[int] = None

    @field_validator("published_year")
    @classmethod
    def validate_year(cls, v):
        if v is not None and not (1800 <= v <= CURRENT_YEAR):
            raise ValueError("Year must be between 1800 and current year")
        return v
