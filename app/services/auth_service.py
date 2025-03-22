from datetime import datetime, timedelta
from jose import JWTError, jwt
from bcrypt import checkpw
from sqlmodel import select, Session
from uuid import uuid4

from app.models.user import User
from app.models.token_session import TokenSession
from app.settings import settings


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return checkpw(plain_password.encode(), hashed_password.encode())


def authenticate_user(db: Session, username: str, password: str) -> User | None:
    statement = select(User).where(User.username == username)
    user = db.exec(statement).first()
    if not user or not verify_password(password, user.password):
        return None
    return user


def create_token(data: dict, expires_delta: timedelta, token_type: str):
    to_encode = data.copy()
    to_encode.update({
        "exp": datetime.utcnow() + expires_delta,
        "iat": datetime.utcnow(),
        "type": token_type
    })
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(user_id: int) -> str:
    return create_token({"sub": str(user_id)}, timedelta(minutes=settings.ACCESS_EXPIRE_MINUTES), "access")

def create_refresh_token(user_id: int) -> str:
    return create_token({"sub": str(user_id)}, timedelta(days=settings.REFRESH_EXPIRE_DAYS), "refresh")
