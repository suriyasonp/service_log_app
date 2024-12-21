from sqlalchemy import Column, String, DateTime, ForeignKey
from database.base import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID  # Compatible with SQLite
from datetime import datetime

class Customer(Base):
    __tablename__ = "customers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    created_on = Column(DateTime, default=datetime.now)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    modified_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    modified_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))