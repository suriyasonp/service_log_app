from typing import List
from fastapi import APIRouter, Depends, HTTPException # type: ignore
from sqlalchemy.orm import Session # type: ignore
from auth.authen import oauth2_scheme
from database.db import SessionLocal
from models.user import User
from schemas.user_schema import UserCreate, UserResponse
from passlib.context import CryptContext # type: ignore
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

@router.post("", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
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

@router.get("", response_model=List[UserResponse])
def get_users(username: str = None, fullname: str = None, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    
    """_summary_ Retrive a list of all users or filter by username or fullname.

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    
    query = db.query(User)
    
    try:
        if username:
            query = query.filter(User.username.ilike(f"%{username}%"))
        if fullname:
            query = query.filter(User.fullname.ilike(f"%{fullname}%"))
        
        users = query.all()
    except Exception as e:
        logger.error(f"Error retrieving users: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving users.")
    return users