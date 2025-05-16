from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette import status

from application.apis.models.admin_model import Administrators
from application.apis.persistence.admin_persistence import create_admins_persistence, get_admins_by_email, \
    get_admins_all_persistence, delete_admin_persistence
from application.apis.schemas.id_schema import IdentifierEntitySchema
from application.apis.schemas.pageable_schema import PageableSchema


def get_admins_all_action(db: Session, page: PageableSchema):
    try:
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail={"message": "Success", "data": get_admins_all_persistence(db, page)}
        )
    except SQLAlchemyError as se:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Database failure", "info": str(se)}
        )

def delete_admin_action(identify : IdentifierEntitySchema, db:Session):
    try:
        print("Reach Action")
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail={"message": delete_admin_persistence(identify, db)}
        )
    except SQLAlchemyError as se:
        print("Error: "+str(se))
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Database failure", "info": str(se)}
        )

def create_admin_action(admin: Administrators, db: Session):
    try:
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail={"message": create_admins_persistence(admin, db)}
        )
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": str(err)}
        )
    except SQLAlchemyError as se:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Database failure", "info": str(se)}
        )
