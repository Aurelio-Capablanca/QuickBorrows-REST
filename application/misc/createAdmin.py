from sqlalchemy.orm import Session
from application.database.session import SessionLocal
from application.apis.models.adminmodel import Administrators
from application.core.security import hash_password
from datetime import datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def create_initial_admin():
    db: Session = SessionLocal()
    try:
        email = "admin@example.com"
        existing = db.query(Administrators).filter_by(adminemail=email).first()
        if existing:
            print("Admin already exists.")
            return

        admin = Administrators(
            adminname="Super",
            adminlastname="Admin",
            adminemail=email,
            adminpass=hash_password("supersecurepassword"),
            adminphone="1234567890",
            adminstatus=True,
            datecreated=datetime.now()
        )
        db.add(admin)
        db.commit()
        print("Admin created successfully.")
    finally:
        db.close()

if __name__ == "__main__":
    create_initial_admin()
