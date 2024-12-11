class Book:
    id: int
    title: str
    author: str

    def __init__(self, id: int, title: str, author: str):
        self.id = id
        self.title = title
        self.author = author
