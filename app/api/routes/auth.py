from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from jose import jwt, JWTError


from app.db.database import get_session
from app.services.auth_service import authenticate_user, create_access_token, create_refresh_token
from app.schemas.auth_schema import Token
from app.schemas.user_schema import UserCreate
from app.services.user_service import create_user
from app.settings import settings
from app.utils import exceptions


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token)
def register(user_data: UserCreate, db: Session = Depends(get_session)):
    user = create_user(db, user_data)
    token = create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise exceptions.IncorrectUsernamelOrPasswordException

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    response = JSONResponse({"access_token": access_token, "token_type": "bearer"})
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=60 * 60 * 24 * 7
    )
    return response

@router.post("/refresh", response_model=Token)
def refresh_token(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise exceptions.MissingRefreshToken

    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
        if payload.get("type") != "refresh":
            raise exceptions.InvalidTokenFormatException
        user_id = int(payload.get("sub"))
    except JWTError:
        raise exceptions.TokenRefreshInvalidFormatException

    new_access = create_access_token(user_id)
    return {"access_token": new_access, "token_type": "bearer"}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("refresh_token")
    return {"msg": "Logged out"}