from fastapi import FastAPI, Path, Query, HTTPException
from .models.book import Book
from .models.bookrequest import BookRequest
from starlette import status
from sqlalchemy import or_
from .database import engine, session
from typing import Optional

app = FastAPI()

Book.metadata.create_all(bind=engine)


@app.get("/books", status_code=status.HTTP_200_OK)
def getAllBooks():
    books = session.query(Book).all()

    return books


@app.get("/book/{id}", status_code=status.HTTP_200_OK)
def getBookById(id: int = Path(gt=0)):
    book = session.query(Book).filter(Book.id == id).first()

    if book is None:
        return HTTPException(status_code=404, detail="Book not found")

    return book


@app.get("/books/", status_code=status.HTTP_200_OK)
def getBooksByTitle(
    title: Optional[str] = Query(None, min_length=3, max_length=100),
    author: Optional[str] = Query(None, min_length=3, max_length=100)
):
    filters = []
    if title:
        filters.append(Book.title.ilike(f"%{title}%"))
    if author:
        filters.append(Book.author.ilike(f"%{author}%"))

    if filters:
        books = session.query(Book).filter(or_(*filters)).all()
    else:
        books = session.query(Book).all()

    return books


@app.post("/book", status_code=status.HTTP_201_CREATED)
def addBook(request: BookRequest):
    book = Book(**request.model_dump())

    session.add(book)
    session.commit()


@app.put("/book/{id}", status_code=status.HTTP_204_NO_CONTENT)
def updateBook(request: BookRequest, id: int = Path(gt=0)):
    book = session.query(Book).filter(Book.id == id).first()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    book.title = request.title
    book.author = request.author

    session.commit()


@app.delete("/book/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteBook(id: int = Path(gt=0)):
    book = session.query(Book).filter(Book.id == id).first()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    session.delete(book)
    session.commit()
