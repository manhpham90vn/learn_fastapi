from fastapi import FastAPI, Path, Query, HTTPException, Depends
from typing import Annotated
from .models.book import Book
from .models.bookrequest import BookRequest
from starlette import status
from sqlalchemy import or_
from sqlalchemy.orm import Session
from .database import engine, SessionLocal
from typing import Optional

app = FastAPI()

Book.metadata.create_all(bind=engine)


def getDatabase():
    session = SessionLocal()

    try:
        yield session
    except Exception as e:
        print("Database not connected", e)
        raise HTTPException(status_code=500, detail="Database not connected")
    finally:
        session.close()


dbDepends = Annotated[Session, Depends(getDatabase)]


@app.get("/books", status_code=status.HTTP_200_OK)
def getAllBooks(db: dbDepends):

    return db.query(Book).all()


@app.get("/book/{id}", status_code=status.HTTP_200_OK)
def getBookById(db: Annotated[Session, Depends(getDatabase)], id: int = Path(gt=0)):
    book = db.query(Book).filter(Book.id == id).first()

    if book is None:
        return HTTPException(status_code=404, detail="Book not found")

    return book


@app.get("/books/", status_code=status.HTTP_200_OK)
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


@app.post("/book", status_code=status.HTTP_201_CREATED)
def addBook(db: dbDepends, request: BookRequest):
    book = Book(**request.model_dump())

    db.add(book)
    db.commit()
    db.refresh(book)


@app.put("/book/{id}", status_code=status.HTTP_204_NO_CONTENT)
def updateBook(db: dbDepends, request: BookRequest, id: int = Path(gt=0)):
    book = db.query(Book).filter(Book.id == id).first()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    book.title = request.title
    book.author = request.author

    db.commit()


@app.delete("/book/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteBook(db: dbDepends, id: int = Path(gt=0)):
    book = db.query(Book).filter(Book.id == id).first()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()
