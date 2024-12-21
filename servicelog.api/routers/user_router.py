from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import SessionLocal
from models.user import User
from schemas.user_schema import UserCreate, UserResponse
from passlib.context import CryptContext
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating user: {user.username}")
    db_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(status_code=400, detail="Username already registered")
        if db_user.email == user.email:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        username=user.username,
        fullname=user.fullname,
        email=user.email,
        password=hash_password(user.password), 
        is_admin=False,
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        db.rollback()  # Rollback any changes if an error occurs
        raise HTTPException(status_code=500, detail="An error occurred while creating the user.")

    return new_user