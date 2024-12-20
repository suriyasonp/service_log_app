from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base

DATABASE_URL = "sqlite:///./servicelog.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    import models.user
    import models.customer
    Base.metadata.create_all(bind=engine)

init_db()