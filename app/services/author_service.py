from sqlmodel import Session, select
from fastapi import HTTPException
from app.models.book import Author
from app.schemas.book_schema import AuthorCreate


def create_author(db: Session, author_data: AuthorCreate) -> Author:
    existing = db.exec(select(Author).where(Author.name == author_data.name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Author already exists")

    author = Author(name=author_data.name)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def get_all_authors(db: Session):
    return db.exec(select(Author)).all()


def get_author_by_id(db: Session, author_id: int) -> Author:
    author = db.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


def delete_author(db: Session, author_id: int):
    author = db.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    db.delete(author)
    db.commit()
    return {"detail": "Author deleted"}
