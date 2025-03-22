from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class BookGenreLink(SQLModel, table=True):
    book_id: Optional[int] = Field(default=None, foreign_key="book.id", primary_key=True)
    genre_id: Optional[int] = Field(default=None, foreign_key="genre.id", primary_key=True)

class Author(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False, unique=True)

    books: List["Book"] = Relationship(back_populates="author")

class Genre(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(index=True, nullable=False, unique=True)

    books: List["Book"] = Relationship(back_populates="genres", link_model=BookGenreLink)

class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, nullable=False)
    published_year: int = Field(index=True)

    author_id: int = Field(foreign_key="author.id")

    author: Optional[Author] = Relationship(back_populates="books")
    genres: List["Genre"] = Relationship(back_populates="books", link_model=BookGenreLink)
