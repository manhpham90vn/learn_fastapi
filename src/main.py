from fastapi import FastAPI
from .routers.auth import router as auth_router
from .routers.book import router as book_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(book_router)
