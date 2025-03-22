from fastapi import status, HTTPException

UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Користувач вже існує'
)

UserNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Користувача не знайдено'
)

GroupAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Група вже існує'
)

IncorrectUsernamelOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Невірні юзернейм чи пароль'
)

MissingRefreshToken = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Пропущений рефреш токен'
)

InvalidTokenFormatException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='Невірний формат токена'
)

TokenRefreshInvalidFormatException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Невірний рефреш токен'
)


DeveloperError = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail='Програміст рука не туда'
)

InvalidDataException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Невірно введені дані"
)

InvalidPatchedUsername = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Такий юзернейм вже використовується"
)

InvalidPatchedEmail = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Такий емейл вже використовується"
)