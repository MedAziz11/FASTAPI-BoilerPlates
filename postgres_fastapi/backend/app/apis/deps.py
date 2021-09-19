from sqlalchemy.orm.session import Session
from app.core.database import SessionLocal

from typing import Generator


def get_db()-> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        
