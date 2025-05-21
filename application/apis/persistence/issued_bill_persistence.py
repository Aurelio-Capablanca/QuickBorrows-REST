from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, selectinload

from application.apis.models.borrow_model import Borrows
from application.apis.models.issued_bill_model import IssuedBill
from application.apis.schemas.id_schema import IdentifierEntitySchema


def create_issued_bills(bills: list[IssuedBill], db: Session):
    try:
        db.add_all(bills)
        db.flush()
        for bill in bills:
            db.refresh(bill)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception("Database error during borrow creation: " + str(e))
    return "Bills Created!"


def get_all_bills_by_borrow(id_borrow: IdentifierEntitySchema, db: Session):
    return db.query(IssuedBill).filter(IssuedBill.idborrow == id_borrow.identity).all()


def delete_issued_bills(id_borrow: int, db: Session):
    statement = delete(IssuedBill).where(IssuedBill.idborrow == id_borrow)
    try:
        db.execute(statement)
        db.flush()
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception("Database error during issued bills deletion: " + str(e))
