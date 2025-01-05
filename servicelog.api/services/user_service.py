from http.client import HTTPException
from schemas.user_schema import UserCreate
from sqlalchemy.orm import Session # type: ignore
import logging

from models.user import User
from services.password_service import get_password_hash

logger = logging.getLogger(__name__)

def get_user_logging_in(username: str, password: str, db: Session):
    hashed_password = get_password_hash(password)
    user = db.query(User).filter(User.username == username and User.password == hashed_password).first()
    return user

def get_user(username: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    return user

def query_users(db: Session, username: str = None, fullname: str = None, is_admin: bool = None):
    query = db.query(User)

    try:
        if username:
            query = query.filter(User.username == username)
        if fullname:
            query = query.filter(User.fullname == fullname)
        if is_admin:
            query = query.filter(User.is_admin == is_admin)
        
        users = query.all()
    except Exception as e:
        logger.error(f"Error retrieving users: {str(e)}")

    return users

def create_new_user(db: Session, user: UserCreate):
    try:
        db_user = db.query(User).filter(
            (User.username == user.username) | (User.email == user.email) | (User.fullname == user.fullname)
        ).first()
        if db_user:
            raise HTTPException(
                status_code=400,
                detail="This account has been already registered",
            )
        
        new_user = User(
            username=user.username,
            fullname=user.fullname,
            email=user.email, 
            password=get_password_hash(user.password),
            is_admin=False)
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while creating user." + str(e)
        )

    return new_user
