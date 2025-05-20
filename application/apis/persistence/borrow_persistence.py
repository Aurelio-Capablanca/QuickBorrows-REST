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
                borrow.totalpayment = borrow.borrowamount + ((borrow.borrowamount * borrow.percentagetax) / 100)
            db.add(borrow)
            db.commit()
            db.refresh(borrow)
            return {"isUpdate": False, "perform": False, "message": "Borrow Created"}
        borrow_get = (db.query(Borrows).filter(Borrows.idborrow == borrow.idborrow).first())
        if not borrow_get:
            raise ValueError("Borrow Not found")
        perform_other_actions = False
        if borrow.percentagetax is not borrow_get.percentagetax or borrow.borrowamount is not borrow_get.borrowamount:
            perform_other_actions = True
            borrow.totalpayment = borrow_get.borrowamount + ((borrow_get.borrowamount * borrow_get.percentagetax) / 100)
        else:
            perform_other_actions = False
            borrow.totalpayment = borrow_get.totalpayment
        borrow.datetaken = borrow_get.datetaken
        db.merge(borrow)
        db.commit()
        return {"isUpdate": True, "perform": perform_other_actions, "message": "Borrow Updated"}
    except SQLAlchemyError as err:
        db.rollback()
        raise SQLAlchemyError("Database Operation Failed by :" + err.code)


def get_all_borrows_persistence(page: PageableSchema, db: Session):
    return db.query(Borrows).offset(page.page).limit(page.limit).all()


def get_one_borrow_persistence(identify: IdentifierEntitySchema, db: Session):
    return db.query(Borrows).filter(Borrows.idborrow == identify.identity).first()


def delete_borrow_persistence(identify: IdentifierEntitySchema, db: Session):
    borrow = db.query(Borrows).filter(Borrows.idborrow == identify.identity).first()
    if borrow:
        borrow.isactive = False
        db.merge(borrow)
        db.commit()
        return "Borrow Deleted!"
    return "Borrow Not Deleted!"
