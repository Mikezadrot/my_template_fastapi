from fastapi import FastAPI
from app.api.routes.users import router as user_router
from app.api.routes.auth import router as auth_router
from app.api.routes.genre import router as genre_router
from app.api.routes.author import router as author_router
from app.api.routes.book import router as book_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(author_router)
app.include_router(genre_router)
app.include_router(book_router)

