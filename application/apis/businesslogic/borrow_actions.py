from operator import concat

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette import status

from application.apis.models.borrow_model import Borrows
from application.apis.models.payment_plan_model import PaymentPlan
from application.apis.schemas.borrow_schema import BorrowRequest
from application.apis.schemas.id_schema import IdentifierEntitySchema
from application.apis.schemas.pageable_schema import PageableSchema
from application.apis.persistence.borrow_persistence import get_all_borrows_persistence, get_one_borrow_persistence, \
    delete_borrow_persistence, save_borrow_persistence
from application.apis.businesslogic.abstraction.payment_plan_calculations import calculate_payment_plan
from application.database.session import engine
from application.apis.persistence.payment_plan_persistence import save_payment_plan_persistence
from application.apis.persistence.issued_bill_persistence import create_issued_bills, delete_issued_bills


def save_borrow_actions(request: BorrowRequest, db: Session):
    try:
        borrow = Borrows(**request.borrow.model_dump())
        bill_conditions = request.billconditions
        try:
            borrows = save_borrow_persistence(borrow, db)
            borrow_entity = borrows["entity"]
            borrow_message = borrows["message"]
            is_update = borrows["isUpdate"]
            perform = borrows["perform"]
            plan = str
            bill = str
            if not is_update or perform:
                plan = save_payment_plan_persistence(
                    PaymentPlan(duedateplan=borrow_entity.duedate, idborrow=borrow_entity.idborrow), db)
                plan_entity = plan["entity"]
                if perform:
                    delete_issued_bills(plan_entity.idplan, db)
                bills = calculate_payment_plan(borrow_entity.totalpayment, bill_conditions.numpayments,
                                               bill_conditions.paymentsof, bill_conditions.generatetofill,
                                               plan_entity.idplan, borrow_entity.duedate)
                bill = create_issued_bills(bills, db)
            message = borrow_message, " And ", plan["message"], " And ", bill
            #session.commit()
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
