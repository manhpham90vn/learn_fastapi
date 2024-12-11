from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:admin@localhost:3306/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URI)

try:
    engine.connect()
    print("Database connected")
except Exception as e:
    print("Database not connected", e)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
