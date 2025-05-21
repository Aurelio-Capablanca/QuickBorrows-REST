from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from application.apis.businesslogic.borrow_actions import save_borrow_actions, get_all_borrows_actions, \
    get_one_borrow_action, delete_borrow_action
from application.apis.schemas.borrow_schema import BorrowRequest
from application.apis.schemas.id_schema import IdentifierEntitySchema
from application.apis.schemas.pageable_schema import PageableSchema
from application.authentication.jwt_dependency import get_current_user
from application.database.session import get_db

router = APIRouter()


@router.post("/api/borrows/save")
def save_borrows_controller(request: BorrowRequest, db: Session = Depends(get_db),
                            current_user=Depends(get_current_user)):
    return save_borrow_actions(request, db)


@router.get("/api/borrows/get-all")
def get_all_borrows_controller(page: PageableSchema, db: Session = Depends(get_db),
                               current_user=Depends(get_current_user)):
    return get_all_borrows_actions(page, db)


@router.get("/api/borrows/get-one")
def get_one_borrow_controller(identifier: IdentifierEntitySchema, db: Session = Depends(get_db),
                              current_user=Depends(get_current_user)):
    return get_one_borrow_action(identifier, db)


@router.post("/api/borrows/delete")
def delete_borrow_controller(identifier: IdentifierEntitySchema, db: Session = Depends(get_db),
                              current_user=Depends(get_current_user)):
    return delete_borrow_action(identifier, db)