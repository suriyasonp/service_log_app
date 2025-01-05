from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class LoginResponse(BaseModel):
    id: UUID
    username: str
    access_token: str
    token_type: str = "bearer"
    login_time: datetime