from sqlmodel import Session, select
from fastapi import HTTPException
from app.models.book import Book, Genre, BookGenreLink
from app.schemas.book_schema import BookCreate, BookUpdate


def create_book(db: Session, book_data: BookCreate) -> Book:
    statement = select(Book).where(Book.title == book_data.title, Book.author_id == book_data.author_id)
    existing = db.exec(statement).first()
    if existing:
        raise HTTPException(status_code=400, detail="Book with this title and author already exists")

    genres = db.exec(select(Genre).where(Genre.name.in_(book_data.genre_names))).all()
    if len(genres) != len(book_data.genre_names):
        raise HTTPException(status_code=400, detail="One or more genres not found")

    book = Book(
        title=book_data.title,
        published_year=book_data.published_year,
        author_id=book_data.author_id,
        genres=genres
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_book_by_id(db: Session, book_id: int) -> Book:
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


def get_all_books(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    title: str = None,
    author_id: int = None,
    genre_names: list = None,
    sort_by: str = "title"
):
    statement = select(Book)

    if title:
        statement = statement.where(Book.title.ilike(f"%{title}%"))
    if author_id:
        statement = statement.where(Book.author_id == author_id)

    if genre_names:
        genre_subquery = select(BookGenreLink.book_id).join(Genre).where(Genre.name.in_(genre_names)).subquery()
        statement = statement.where(Book.id.in_(select(genre_subquery.c.book_id)))

    if sort_by in {"title", "published_year"}:
        statement = statement.order_by(getattr(Book, sort_by))

    statement = statement.offset(skip).limit(limit)
    return db.exec(statement).all()


def update_book(db: Session, book_id: int, updates: BookUpdate) -> Book:
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    update_data = updates.model_dump(exclude_unset=True)
    if "genre_names" in update_data:
        genre_names = update_data.pop("genre_names")
        genres = db.exec(select(Genre).where(Genre.name.in_(genre_names))).all()
        if len(genres) != len(genre_names):
            raise HTTPException(status_code=400, detail="One or more genres not found")
        book.genres = genres

    for key, value in update_data.items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book_id: int):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"detail": "Book deleted"}