from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette import status

from application.apis.models.borrow_funds_model import BorrowFunds
from application.apis.persistence.borrow_funds_persistence import save_funds_persistence, get_all_founds
from application.apis.schemas.pageable_schema import PageableSchema


def create_founds_action(founds: BorrowFunds, id_admin: int, db: Session):
    print("At Actions: ",id_admin)
    try:
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail={"message": save_funds_persistence(founds, id_admin, db)}
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


def get_founds_all_action(page: PageableSchema, db: Session):
    try:
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail={"message": "Success", "data": get_all_founds(page, db)}
        )
    except SQLAlchemyError as se:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Database failure", "info": str(se)}
        )