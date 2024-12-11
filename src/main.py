from fastapi import FastAPI
from .models.book import Book
from .database import engine
from .routers.auth import router as auth_router
from .routers.book import router as book_router

app = FastAPI()

Book.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(book_router)
