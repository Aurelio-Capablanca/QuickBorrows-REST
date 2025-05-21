from datetime import datetime, timezone

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from application.apis.models.borrow_funds_model import BorrowFunds
from application.apis.models.borrow_funds_historic_model import BorrowFundsHistoric
from application.apis.schemas.pageable_schema import PageableSchema


def save_funds_persistence(funds: BorrowFunds, id_admin: int, db: Session):
    try:
        if funds.idfound is None:
            funds.datecreated = datetime.now(timezone.utc)
            funds.idadministrator = id_admin
            funds.isinput = True
            funds.initialamount = 0
            db.add(funds)
            db.commit()
            db.refresh(funds)
            return "Found Added"
        fund_get = db.query(BorrowFunds).filter(BorrowFunds.idfound == funds.idfound).first()
        if not fund_get:
            raise ValueError("Not found")
        funds.datecreated = fund_get.datecreated
        funds.idadministrator = fund_get.idadministrator
        funds.initialamount = fund_get.initialamount
        if funds.isinput:
            funds.amountfound += fund_get.amountfound
        else:
            funds.amountfound -= fund_get.amountfound
        past_founds : float = fund_get.amountfound
        id_origin : int = fund_get.idfound
        historic = BorrowFundsHistoric(amountfound=funds.amountfound, pastamount=past_founds,
                                       datecreated=datetime.now(timezone.utc), idorigin=id_origin, isinput = funds.isinput, idadministrator=id_admin)
        db.merge(funds)
        db.add(historic)
        db.commit()
        db.refresh(historic)
        return "Found Updated"
    except SQLAlchemyError as err:
        db.rollback()
        raise SQLAlchemyError("Database operation Failed by :" + str(err))


def get_all_founds(page: PageableSchema, db: Session):
    return db.query(BorrowFundsHistoric).offset(page.page).limit(page.limit).all()