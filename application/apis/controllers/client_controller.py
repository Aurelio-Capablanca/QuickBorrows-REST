from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from application.apis.businesslogic.client_actions import create_client_action, get_one_client_action, \
    get_all_clients_action, delete_clients_action
from application.apis.models.client_model import Clients
from application.apis.schemas.client_schema import ClientsSchema
from application.apis.schemas.id_schema import IdentifierEntitySchema
from application.apis.schemas.pageable_schema import PageableSchema
from application.authentication.jwt_dependency import get_current_user
from application.database.session import get_db

router = APIRouter()


@router.post("/api/clients/create")
def create_client_controller(client: ClientsSchema, db: Session = Depends(get_db),
                             current_user=Depends(get_current_user)):
    return create_client_action(Clients(**client.model_dump()), db)


@router.get("/api/clients/get-one")
def get_one_client_controller(identify: IdentifierEntitySchema, db: Session = Depends(get_db),
                              current_user=Depends(get_current_user)):
    return get_one_client_action(identify, db)


@router.get("/api/clients/get-all")
def get_all_clients_controller(page: PageableSchema, db: Session = Depends(get_db),
                               current_user=Depends(get_current_user)):
    return get_all_clients_action(page, db)


@router.post("/api/clients/delete")
def delete_one_client(identify: IdentifierEntitySchema, db: Session = Depends(get_db),
                      current_user=Depends(get_current_user)):
    return delete_clients_action(identify, db)
