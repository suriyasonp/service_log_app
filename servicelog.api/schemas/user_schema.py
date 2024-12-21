from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from uuid import UUID
from datetime import datetime

class UserBase(BaseModel):
    username: str
    fullname: str
    email: Optional[EmailStr] = None

    @validator('email', pre=True, always=True)
    def set_empty_email_to_none(cls, v):
        if v == "":
            return None
        return v

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: UUID
    is_admin: bool
    created_on: datetime
    modified_on: datetime

    class Config:
            orm_mode = True