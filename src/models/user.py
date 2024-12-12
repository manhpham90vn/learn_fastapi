from .base import Base
from sqlalchemy import Column, Integer, String, Boolean


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    hashed_password = Column(String(100))
    is_active = Column(Boolean, default=True)
    role = Column(String(100))

    def __init__(self, email: str, first_name: str, last_name: str, hashed_password: str, role: str, is_active: bool = True):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.hashed_password = hashed_password
        self.role = role
        self.is_active = is_active
