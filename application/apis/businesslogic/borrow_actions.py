from operator import concat

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette import status

from application.apis.models.borrow_model import Borrows
from application.apis.schemas.borrow_schema import BorrowRequest
from application.apis.schemas.id_schema import IdentifierEntitySchema
from application.apis.schemas.pageable_schema import PageableSchema
from application.apis.persistence.borrow_persistence import get_all_borrows_persistence, get_one_borrow_persistence, \
    delete_borrow_persistence, save_borrow_persistence, change_due_date_borrow_persistence
from application.apis.businesslogic.abstraction.payment_plan_calculations import calculate_issued_bill
from application.apis.persistence.issued_bill_persistence import create_issued_bills, delete_issued_bills


def save_borrow_actions(request: BorrowRequest, db: Session):
    try:
        borrow = Borrows(**request.borrow.model_dump())
        bill_conditions = request.billconditions
        try:
            borrows = save_borrow_persistence(borrow, db)
            borrow_message = borrows["message"]
            is_update = borrows["isUpdate"]
            perform = borrows["perform"]
            print("is about to perform ? ", perform)
            bill: str = ""
            if not is_update or perform:
                if perform:
                    delete_issued_bills(borrow.idborrow, db)
                bills = calculate_issued_bill(borrow.totalpayment, bill_conditions.numpayments,
                                              bill_conditions.paymentsof, bill_conditions.generatetofill,
                                              borrow.idborrow, borrow.datetaken)
                bill = create_issued_bills(bills, db)
                change_due_date_borrow_persistence(bills[len(bills) - 1].duedate, borrow, db)
            message = borrow_message, " And ", bill
            db.commit()
            return HTTPException(
                status_code=status.HTTP_200_OK,
                detail={"message": "Success", "data": message}
            )
        except Exception:
            db.rollback()
            raise
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": str(err)})
    except SQLAlchemyError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": concat("Database Failure", str(err))})


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
