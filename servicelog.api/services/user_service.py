from sqlalchemy.orm import Session
from fastapi import Depends
from database.db import SessionLocal

from models.user import User

from services.password_service import get_password_hash

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_logging_in(username: str, password: str, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(password)
    user = db.query(User).filter(User.username == username and User.password == hashed_password).first()
    return user

def get_user(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    return user
