from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base

DATABASE_URL = "sqlite:///./servicelog.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    from models.user import User
    from models.customer import Customer
    from models.machine_model import MachineModel

    print("Registered tables:", Base.metadata.tables.keys())

    Base.metadata.create_all(bind=engine)

init_db()