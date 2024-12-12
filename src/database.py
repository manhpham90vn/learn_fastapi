from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi import HTTPException, Depends
from typing import Annotated
from sqlalchemy.orm import Session

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:admin@localhost:3306/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URI)

try:
    engine.connect()
    print("Database connected")
except Exception as e:
    print("Database not connected", e)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def getDatabase():
    session = SessionLocal()

    try:
        yield session
    except Exception as e:
        print("Database error", e)
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        session.close()


dbDepends = Annotated[Session, Depends(getDatabase)]
