from datetime import datetime, timezone

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from application.apis.models.admin_model import Administrators
from application.apis.schemas.pageable_schema import PageableSchema
from application.core.security import hash_password


def get_admins_by_email(email: str, db: Session):
    return db.query(Administrators).filter(Administrators.adminemail == email).first()


def create_admins_persistence(admin: Administrators, db: Session):
    try:
        if admin.idadministrator is None:
            admin.datecreated = datetime.now(timezone.utc)
            admin.adminpass = hash_password(admin.adminpass)
            db.add(admin)
            db.commit()
            db.refresh(admin)
            return "Admin Created"
        admin_get = (db.query(Administrators)
                     .filter(Administrators.idadministrator == admin.idadministrator)
                     .first())
        if not admin_get:
            return ValueError("Admin Not Found")
        admin.datecreated = admin_get.datecreated
        admin.adminpass = admin.adminpass
        db.merge(admin)
        db.commit()
        db.close()
        return "Admin Updated"
    except SQLAlchemyError:
        db.rollback()
        return SQLAlchemyError("Database operation failed")


def get_admins_all_persistence(db: Session, page : PageableSchema):
    return db.query(Administrators).offset(page.page).limit(page.limit).all()
