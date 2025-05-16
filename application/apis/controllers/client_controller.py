from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from application.apis.businesslogic.client_actions import create_client_action
from application.apis.schemas.client_schema import Clients
from application.authentication.jwt_dependency import get_current_user
from application.database.session import get_db

router = APIRouter()


@router.post("/api/clients/create")
def create_client_controller(client: Clients, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return create_client_action(Clients(**client.model_dump()),db)