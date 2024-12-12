from fastapi import APIRouter
from fastapi import Path, Query, HTTPException, Depends
from typing import Annotated
from ..models.book import Book
from ..models.requests.book_request import BookRequest
from starlette import status
from sqlalchemy import or_
from sqlalchemy.orm import Session
from typing import Optional
from ..routers.auth import router
from ..database import dbDepends, getDatabase

router = APIRouter(prefix="/book", tags=["book"])


@router.get("/", status_code=status.HTTP_200_OK)
def getAllBooks(db: dbDepends):

    return db.query(Book).all()


@router.get("/{id}", status_code=status.HTTP_200_OK)
def getBookById(db: Annotated[Session, Depends(getDatabase)], id: int = Path(gt=0)):
    book = db.query(Book).filter(Book.id == id).first()

    if book is None:
        return HTTPException(status_code=404, detail="Book not found")

    return book


@router.get("/", status_code=status.HTTP_200_OK)
def getBooksByTitle(
    db: dbDepends,
    title: Optional[str] = Query(None, min_length=3, max_length=100),
    author: Optional[str] = Query(None, min_length=3, max_length=100)
):
    filters = []
    if title:
        filters.append(Book.title.ilike(f"%{title}%"))
    if author:
        filters.append(Book.author.ilike(f"%{author}%"))

    if filters:
        books = db.query(Book).filter(or_(*filters)).all()
    else:
        books = db.query(Book).all()

    return books


@router.post("/", status_code=status.HTTP_201_CREATED)
def addBook(db: dbDepends, request: BookRequest):
    book = Book(**request.model_dump())

    db.add(book)
    db.commit()
    db.refresh(book)


@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def updateBook(db: dbDepends, request: BookRequest, id: int = Path(gt=0)):
    book = db.query(Book).filter(Book.id == id).first()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    book.title = request.title
    book.author = request.author

    db.commit()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteBook(db: dbDepends, id: int = Path(gt=0)):
    book = db.query(Book).filter(Book.id == id).first()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()
