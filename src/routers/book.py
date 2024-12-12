from fastapi import APIRouter
from fastapi import Path, Query, HTTPException
from ..models.book import Book
from ..models.requests.book_request import BookRequest
from starlette import status
from sqlalchemy import or_
from typing import Optional
from ..routers.auth import router
from ..dependency import userDepends, dbDepends

router = APIRouter(prefix="/book", tags=["book"])


@router.get("", status_code=status.HTTP_200_OK)
def getAllBooks(user: userDepends, db: dbDepends):

    return db.query(Book).filter(Book.owner_id == user.get("id")).all()


@router.get("/{id}", status_code=status.HTTP_200_OK)
def getBookById(user: userDepends, db: dbDepends, id: int = Path(gt=0)):
    book = db.query(Book).filter(Book.id == id).filter(
        Book.owner_id == user.get("id")).first()

    if book is None:
        return HTTPException(status_code=404, detail="Book not found")

    return book


@router.get("/", status_code=status.HTTP_200_OK)
def getBooksByTitle(
    user: userDepends,
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
        books = db.query(Book).filter(
            Book.id == user.get("id")).filter(or_(*filters)).all()
    else:
        books = db.query(Book).filter(Book.id == user.get("id")).all()

    return books


@router.post("/", status_code=status.HTTP_201_CREATED)
def addBook(user: userDepends, db: dbDepends, request: BookRequest):
    book = Book(**request.model_dump(), owner_id=user.get("id"))

    db.add(book)
    db.commit()
    db.refresh(book)


@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def updateBook(user: userDepends, db: dbDepends, request: BookRequest, id: int = Path(gt=0)):
    book = db.query(Book).filter(Book.id == id).filter(
        Book.id == user.get("id")).first()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    book.title = request.title
    book.author = request.author

    db.commit()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteBook(user: userDepends, db: dbDepends, id: int = Path(gt=0)):
    book = db.query(Book).filter(Book.id == id).filter(
        Book.id == user.get("id")).first()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()
