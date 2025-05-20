from operator import concat

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette import status

from application.apis.models.borrow_model import Borrows
from application.apis.schemas.id_schema import IdentifierEntitySchema
from application.apis.schemas.pageable_schema import PageableSchema
from application.apis.persistence.borrow_persistence import get_all_borrows_persistence, get_one_borrow_persistence, \
    delete_borrow_persistence, save_borrow_persistence
from application.apis.businesslogic.abstraction.payment_plan_calculations import  calculate_payment_plan
from application.database.session import engine


def save_borrow_actions(borrow: Borrows, db: Session):
    try:

        with Session(engine) as session:
            try:
                borrows = save_borrow_persistence(borrow, db)
                ## Missing Payment Plan and Bills issue (call payment plan calculations)
                # calculate_payment_plan(1650, [10, 3], [100, 216.67], False, 0, datetime.now(timezone.utc))

                session.commit()
            except Exception:
                session.rollback()
                raise
    except ValueError as err:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                      detail={"message": str(err)})
    except SQLAlchemyError as err:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                      detail={"message": concat("Database Failure",str(err))})


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
