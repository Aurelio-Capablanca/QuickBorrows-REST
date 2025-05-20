from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from application.apis.models.payment_plan_model import PaymentPlan
from application.apis.schemas.id_schema import IdentifierEntitySchema


def save_payment_plan_persistence(plan: PaymentPlan, db: Session):
    try:
        if plan.idplan is None:
            db.add(plan)
            db.commit()
            db.refresh(plan)
        db.merge(plan)
        db.commit()
    except SQLAlchemyError as err:
        db.rollback()
        raise SQLAlchemyError("Database Operation Failed by : " + err.code)


def see_payment_plan_by_borrow(id_borrow: IdentifierEntitySchema, db: Session):
    return db.query(PaymentPlan).filter(PaymentPlan.idborrow == id_borrow.identity).all()
