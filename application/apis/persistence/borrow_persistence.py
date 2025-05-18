from datetime import datetime, timezone

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from application.apis.models.borrow_model import Borrows
from application.apis.schemas.id_schema import IdentifierEntitySchema
from application.apis.schemas.pageable_schema import PageableSchema


def save_borrow_persistence(borrow: Borrows, db: Session):
    try:
        if borrow.idborrow is None:
            borrow.datetaken = datetime.now(timezone.utc)
            if borrow.percentagetax is None:
                borrow.percentagetax = 10.0
            db.add(borrow)
            db.commit()
            db.refresh(borrow)
            return "Borrow Created"
        borrow_get = (db.query(Borrows).filter(Borrows.idborrow == borrow.idborrow).first())
        if not borrow_get :
            raise ValueError("Borrow Not found")
        borrow.datetaken = borrow_get.datetaken
        #if borrow tax is changed perform a payment plan recalc
        db.commit()
        return "Borrow Updated"
    except SQLAlchemyError as err:
        db.rollback()
        raise SQLAlchemyError("Database Operation Failed by :"+err.code)
