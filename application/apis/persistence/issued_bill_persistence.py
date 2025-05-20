from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, selectinload

from application.apis.models.payment_plan_model import PaymentPlan
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


async def get_all_bills_by_borrow_(id_borrow: IdentifierEntitySchema, db: Session):
    join_tables = (select(IssuedBill)
                   .join(IssuedBill.idplan)
                   .join(PaymentPlan.idborrow)
                   .options(selectinload(IssuedBill.idplan).selectinload(PaymentPlan.idborrow))
                   .where(PaymentPlan.idborrow == id_borrow.identity)
                   )
    result = await db.execute(join_tables)
    bills = result.scalar_one_or_none()
    return bills


async def delete_issued_bills(id_plan: int, db: Session):
    statement = delete(IssuedBill).where(IssuedBill.idplan == id_plan)
    await db.execute(statement)
    await db.commit()
