from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from database.base import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID  # Compatible with SQLite
from datetime import datetime
from enums import MachineTypes

class MachineModel(Base):
    __tablename__ = "machine_models"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    machine_type = Column(Enum(MachineTypes), default=MachineTypes.BATCHING_PLANT, nullable=False)
    created_on = Column(DateTime, default=datetime.now)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    modified_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    modified_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))