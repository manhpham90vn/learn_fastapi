from sqlalchemy import Column, Integer, String, ForeignKey

from ..containers import container

Base = container.get_base()


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    author = Column(String(100))
    owner_id = Column(Integer, ForeignKey('users.id'))
