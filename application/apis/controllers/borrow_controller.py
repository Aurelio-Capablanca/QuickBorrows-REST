from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from application.apis.businesslogic.borrow_actions import save_borrow_actions
from application.apis.schemas.borrow_schema import BorrowRequest
from application.authentication.jwt_dependency import get_current_user
from application.database.session import get_db




router = APIRouter()


@router.post("/api/borrows/save")
def save_borrows_controller(request : BorrowRequest, db:Session=Depends(get_db), current_user=Depends(get_current_user)):
    return save_borrow_actions(request, db)