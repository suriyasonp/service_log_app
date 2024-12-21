from passlib.context import CryptContext
from sqlalchemy.orm import sessionmaker
from models.user import User
import db

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Database Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db.engine)

# Function to hash the password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def add_default_admin():
    # Open a session
    session = SessionLocal()
    try:
        # Check if there are any employees
        if not session.query(User).first():
             # Hash the password
            hashed_password = hash_password("1234")
            # Add default admin
            admin = User(
                username="admin", 
                fullname="LTH Admin", 
                email="", 
                password=hashed_password, 
                is_admin=True)
            session.add(admin)
            session.commit()
            session.refresh(admin)
            print(f"Default admin account created. {admin.username}")
        else:
            print("Default admin already exists.")
    finally:
        session.close()

add_default_admin()