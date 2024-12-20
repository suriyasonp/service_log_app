from sqlalchemy.orm import sessionmaker
from user import User

# Database Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def add_default_admin():
    # Open a session
    session = SessionLocal()
    try:
        # Check if there are any employees
        if not session.query(User).first():
            # Add default admin
            admin = User(name="lthadmin", fullname="LTH Admin", email="", password="Lth1234!", is_admin=True)
            session.add(admin)
            session.commit()
            print("Default admin account created.")
        else:
            print("Default admin already exists.")
    finally:
        session.close()