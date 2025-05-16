from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette import status

from application.apis.models.client_model import Clients
from application.apis.persistence.client_persistence import create_clients_persistence
from application.apis.schemas.id_schema import IdentifierEntitySchema
from application.apis.schemas.pageable_schema import PageableSchema


def create_client_action(client: Clients, db: Session):
    try:
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail={"message": create_clients_persistence(client, db)}
        )
    except ValueError as err:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": str(err)}
        )
    except SQLAlchemyError as err:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Database failure", "info": str(err)}
        )
