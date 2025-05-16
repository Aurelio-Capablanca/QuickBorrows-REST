from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from application.apis.models.adminmodel import Administrators


def get_admins_by_email(email: str, db: Session):
    return db.query(Administrators).filter(Administrators.adminemail == email).first()


# adminPass varchar(100) not null,
# dateCreated timestamp default current_timestamp
def create_admins(admin: Administrators, db: Session):
    try:
        if not admin.idadministrator:
            db.add(admin)
            db.commit()
            db.refresh(admin)
            return {"Success": True, "info": "Admin Created"}
        admin_get = (db.query(Administrators)
                     .filter(Administrators.idadministrator == admin.idadministrator)
                     .first())
        if not admin_get:
            return {"Success": False, "info": "Admin Not Found"}
        admin.datecreated = admin_get.datecreated
        admin.adminpass = admin.adminpass
        db.merge(admin)
        db.commit()
        db.close()
        return {"Success": True, "info": "Admin Updated"}
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": "Database operation failed", "info": str(e)}


