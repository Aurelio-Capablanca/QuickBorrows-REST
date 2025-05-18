from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from application.apis.models.admin_model import Administrators
from application.apis.schemas.admin_schema import AdministratorSchema
from application.apis.schemas.id_schema import IdentifierEntitySchema
from application.apis.schemas.pageable_schema import PageableSchema
from application.database.session import get_db
from application.authentication.jwt_dependency import get_current_user
from application.apis.businesslogic.admin_actions import create_admin_action, get_admins_all_action, \
    delete_admin_action, get_one_admin_action

router = APIRouter()


@router.post("/api/admins/create")
def create_admin_controller(admin: AdministratorSchema, db: Session = Depends(get_db),
                            current_user=Depends(get_current_user)):
    return create_admin_action(Administrators(**admin.model_dump()), db)


@router.get("/api/admins/get-all")
def get_all_controller(page: PageableSchema, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_admins_all_action(db, page)


@router.get("/api/admins/get-one")
def get_one_controller(identify: IdentifierEntitySchema, db: Session = Depends(get_db),
                       current_user=Depends(get_current_user)):
    return get_one_admin_action(identify, db)


@router.post("/api/admins/delete")
def delete_one_controller(identifier: IdentifierEntitySchema, db: Session = Depends(get_db),
                          current_user=Depends(get_current_user)):
    print("Reach Controller")
    return delete_admin_action(identifier, db)
