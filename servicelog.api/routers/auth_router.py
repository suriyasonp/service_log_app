from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.db import SessionLocal
from models.user import User
from auth.authen import create_access_token, get_current_user, verify_password, oauth2_scheme, decode_access_token
import logging
from schemas.login_schema import LoginResponse

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
        user = db.query(User).filter(User.username == form_data.username).first()
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
def read_users_me(token: str = Depends(oauth2_scheme)):
    payload = get_current_user(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return {"username": payload.get("username"),
            "access_token": token}