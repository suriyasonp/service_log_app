from datetime import datetime
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.db import SessionLocal
from models.user import User
from auth.authen import create_access_token, get_current_user, oauth2_scheme
from services.password_service import verify_password
from schemas.login_schema import LoginResponse
from schemas.user_schema import UserResponse
from services.user_service import get_user_logging_in, get_user

logger = logging.getLogger(__name__)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/token", response_model=LoginResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        # Check if user exists
        user = get_user_logging_in(form_data.username, form_data.password, db)
        if not user or not verify_password(form_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # Generate token
        access_token = create_access_token(data={"sub": user.username})
    except:
        logger.exception("An error occurred while logging in. Detail:")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while logging in.",
        )
    
    return LoginResponse(
        id=user.id,
        username=user.username,
        access_token=access_token,
        token_type="bearer",
        login_time=datetime.utcnow(),
    )

@router.get("/me")
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = get_current_user(token)
    logged_on_user = get_user(user.get("username"), db)

    if not logged_on_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return UserResponse(
        id=logged_on_user.id,
        username=logged_on_user.username,
        email=logged_on_user.email,
        full_name=logged_on_user.full_name,
        is_active=logged_on_user.is_active,
        created_at=logged_on_user.created_at,
        updated_at=logged_on_user.updated_at,
    )