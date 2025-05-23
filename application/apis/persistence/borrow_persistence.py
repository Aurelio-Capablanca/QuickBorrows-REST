from datetime import datetime, timezone

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from application.apis.models.borrow_model import Borrows
from application.apis.schemas.id_schema import IdentifierEntitySchema
from application.apis.schemas.pageable_schema import PageableSchema


def save_borrow_persistence(borrow: Borrows, db: Session):
    if borrow.idborrow is None:
        borrow.datetaken = datetime.now(timezone.utc)
        print(borrow.percentagetax)
        if borrow.percentagetax is None:
            borrow.percentagetax = 10.0
        borrow.totalpayment = borrow.borrowamount + ((borrow.borrowamount * borrow.percentagetax) / 100)
        db.add(borrow)
        try:
            db.flush()
            db.refresh(borrow)
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception("Database error during borrow creation: " + str(e))
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
    if borrow.percentagetax is None:
        borrow.percentagetax = 10.0
    borrow.datetaken = borrow_get.datetaken
    borrow.duedate = borrow_get.duedate
    merge = borrow
    try:
        db.merge(merge)
        db.flush()
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception("Database error during borrow update: " + str(e))
    return {"isUpdate": True, "perform": perform_other_actions, "message": "Borrow Updated"}


def change_due_date_borrow_persistence(due_date: datetime, borrow: Borrows, db: Session):
    borrow.duedate = due_date
    try:
        db.merge(borrow)
        db.flush()
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception("Database error during borrow update due date: " + str(e))


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
