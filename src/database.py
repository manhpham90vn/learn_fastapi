from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException
from .config import SQLALCHEMY_DATABASE_URI
from sqlalchemy.exc import IntegrityError

engine = create_engine(SQLALCHEMY_DATABASE_URI)

try:
    engine.connect()
    print("Database connected")
except Exception as e:
    print("Database not connected", e)
    raise HTTPException(status_code=500, detail="Database not connected")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def getDatabase():
    session = SessionLocal()

    try:
        yield session
    except Exception as e:
        print("Database error", e)
        raise e
    finally:
        session.close()
