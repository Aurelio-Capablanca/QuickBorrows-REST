from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette import status

from application.apis.schemas.id_schema import IdentifierEntitySchema
from application.apis.schemas.pageable_schema import PageableSchema
from application.apis.persistence.borrow_persistence import get_all_borrows_persistence, get_one_borrow_persistence, \
    delete_borrow_persistence


def get_all_borrows_actions(page: PageableSchema, db: Session):
    try:
        HTTPException(
            status_code=status.HTTP_200_OK,
            detail={"message": "Success", "data": get_all_borrows_persistence(page, db)}
        )
    except SQLAlchemyError as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Database failure", "info": str(err)}
        )


def get_one_borrow_action(identify: IdentifierEntitySchema, db: Session):
    try:
        HTTPException(
            status_code=status.HTTP_200_OK,
            detail={"message": "Success", "data": get_one_borrow_persistence(identify, db)}
        )
    except SQLAlchemyError as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Database failure", "info": str(err)}
        )


def delete_borrow_action(identify: IdentifierEntitySchema, db: Session):
    try:
        HTTPException(
            status_code=status.HTTP_200_OK,
            detail={"message": "Success", "data": delete_borrow_persistence(identify, db)}
        )
    except SQLAlchemyError as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Database failure", "info": str(err)}
        )
