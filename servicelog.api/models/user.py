import uuid
from sqlalchemy.dialects.postgresql import UUID  # Compatible with SQLite
from sqlalchemy import Column, String, Boolean, DateTime
from database.base import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"  # Updated table name
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String, nullable=False)
    fullname = Column(String, nullable=False)
    email = Column(String, nullable=True)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_on = Column(DateTime, default=datetime.utcnow)
    modified_on = Column(DateTime, default=datetime.utcnow)