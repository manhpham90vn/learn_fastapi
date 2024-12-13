from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException
from .containers import container


def get_engine():
    data_base_url = container.data_base_url()
    engine = create_engine(data_base_url)

    try:
        engine.connect()
        print("Database connected")
    except Exception as e:
        print("Database not connected", e)
        raise HTTPException(status_code=500, detail="Database not connected")

    return engine


engine = get_engine()
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
