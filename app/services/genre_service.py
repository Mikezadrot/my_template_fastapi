from sqlmodel import Session, select
from fastapi import HTTPException
from app.models.book import Genre
from app.schemas.book_schema import GenreCreate


def create_genre(db: Session, genre_data: GenreCreate) -> Genre:
    statement = select(Genre).where(Genre.name == genre_data.name)
    existing = db.exec(statement).first()
    if existing:
        raise HTTPException(status_code=400, detail="Genre already exists")

    genre = Genre(name=genre_data.name)
    db.add(genre)
    db.commit()
    db.refresh(genre)
    return genre


def get_all_genres(db: Session):
    return db.exec(select(Genre)).all()


def get_genre_by_id(db: Session, genre_id: int) -> Genre:
    genre = db.get(Genre, genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genre


def delete_genre(db: Session, genre_id: int):
    genre = db.get(Genre, genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    db.delete(genre)
    db.commit()
    return {"detail": "Genre deleted"}
