from ..database import Base
from sqlalchemy import Column, Integer, String


class Book(Base):

    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    author = Column(String(100))
