from sqlmodel import SQLModel, create_engine, Session
from app.settings import settings

from app.models.user import User, Group, UserGroupLink

engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)

def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
