from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from application.apis.businesslogic.borrow_funds_actions import create_founds_action, get_founds_all_action
from application.apis.models.borrow_funds_model import BorrowFunds
from application.apis.schemas.pageable_schema import PageableSchema
from application.database.session import get_db
from application.authentication.jwt_dependency import get_current_user

from application.apis.schemas.borrow_funds_schema import BorrowFundsSchema

router = APIRouter()


@router.post("/api/founds/save")
def save_funds(found: BorrowFundsSchema, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    print(current_user)
    print("ID : ",current_user.idadministrator)
    return create_founds_action(BorrowFunds(**found.model_dump()), current_user.idadministrator, db)


@router.post("/api/founds/get-all")
def save_funds(page: PageableSchema, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_founds_all_action(page, db)
