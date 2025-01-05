from typing import List
from fastapi import APIRouter, Depends, HTTPException # type: ignore
from sqlalchemy.orm import Session # type: ignore
from auth.authen import oauth2_scheme
from database.db import SessionLocal
from models.user import User
from schemas.user_schema import UserCreate, UserResponse
from services.user_service import get_users, create_new_user
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    logger.info(f"Creating user: {user.username}")    
    new_user = create_new_user(db, user)
    return new_user

@router.get("", response_model=List[UserResponse])
def get_users(username: str = None, fullname: str = None, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    
    """_summary_ Retrive a list of all users or filter by username or fullname.

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    
    try:
        users = get_users(db, username, fullname)
    except Exception as e:
        logger.error(f"Error retrieving users: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving users." + str(e))
    return users