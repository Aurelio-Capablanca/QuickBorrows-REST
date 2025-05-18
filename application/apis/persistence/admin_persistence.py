from datetime import datetime, timezone

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from application.apis.models.admin_model import Administrators
from application.apis.schemas.id_schema import IdentifierEntitySchema
from application.apis.schemas.pageable_schema import PageableSchema
from application.core.security import hash_password


def get_admins_by_email(email: str, db: Session):
    return db.query(Administrators).filter(Administrators.adminemail == email).first()

def delete_admin_persistence(identify : IdentifierEntitySchema, db: Session):
    admin = db.query(Administrators).filter(Administrators.idadministrator == identify.identity).first()
    if admin:
        db.delete(admin)
        db.commit()
        return "Admin Deleted"
    return "Admin Not Deleted"

def get_one_admin_persistence(identify : IdentifierEntitySchema, db: Session):
    return db.query(Administrators).filter(Administrators.idadministrator == identify.identity).first()

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
            raise ValueError("Admin Not Found")
        admin.datecreated = admin_get.datecreated
        admin.adminpass = admin_get.adminpass
        db.merge(admin)
        db.commit()
        return "Admin Updated"
    except SQLAlchemyError as err:
        db.rollback()
        raise SQLAlchemyError("Database operation Failed by :"+err.code)


def get_admins_all_persistence(db: Session, page : PageableSchema):
    return db.query(Administrators).offset(page.page).limit(page.limit).all()
