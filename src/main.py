from fastapi import FastAPI, Path, Query, HTTPException
from .models.book import Book
from .models.bookrequest import BookRequest
from starlette import status

app = FastAPI()

books = [
    Book(1, "Harry Potter", "J.K. Rowling"),
    Book(2, "The Lord of the Rings", "J.R.R. Tolkien"),
]


@app.get("/books", status_code=status.HTTP_200_OK)
def getAllBooks():
    return books


@app.get("/book/{id}", status_code=status.HTTP_200_OK)
def getBookById(id: int = Path(gt=0, lt=999)):
    for book in books:
        if book.id == id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.get("/books/", status_code=status.HTTP_200_OK)
def getBooksByTitle(title: str = Query(min_length=3, max_length=100), author: str = Query(min_length=3, max_length=100)):
    return [book for book in books if book.title.casefold() == title.casefold() or book.author.casefold() == author.casefold()]


@app.post("/book", status_code=status.HTTP_201_CREATED)
def addBook(request: BookRequest):
    book = Book(id=len(books) + 1, title=request.title, author=request.author)
    books.append(book)


@app.put("/book/{id}", status_code=status.HTTP_204_NO_CONTENT)
def updateBook(request: BookRequest, id: int = Path(gt=0, lt=999)):
    book_changed = False
    for book in books:
        if book.id == id:
            book.title = request.title
            book.author = request.author
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/book/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteBook(id: int = Path(gt=0, lt=999)):
    book_deleted = False
    for book in books:
        if book.id == id:
            books.remove(book)
            book_deleted = True
    if not book_deleted:
        raise HTTPException(status_code=404, detail="Book not found")
