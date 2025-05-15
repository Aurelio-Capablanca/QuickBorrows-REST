from sqlalchemy.orm import Session

from application.apis.models.adminmodel import Administrators


def get_admins_by_email(email: str, db: Session):
    return db.query(Administrators).filter(Administrators.adminemail == email).first()
