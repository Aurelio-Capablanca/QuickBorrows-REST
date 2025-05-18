from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette import status

from application.apis.models.client_model import Clients
from application.apis.persistence.client_persistence import create_clients_persistence, get_clients_all_persistence, \
    delete_clients_persistence, get_one_client_persistence
from application.apis.schemas.id_schema import IdentifierEntitySchema
from application.apis.schemas.pageable_schema import PageableSchema


def get_one_client_action(identify: IdentifierEntitySchema, db: Session):
    try:
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail={"message": "Success", "data": get_one_client_persistence(identify, db)}
        )
    except SQLAlchemyError as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Database failure", "info": str(err)}
        )


def create_client_action(client: Clients, db: Session):
    try:
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail={"message": create_clients_persistence(client, db)}
        )
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": str(err)}
        )
    except SQLAlchemyError as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Database failure", "info": str(err)}
        )


def get_all_clients_action(identifier: PageableSchema, db: Session):
    try:
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail={"message": "Success", "data": get_clients_all_persistence(identifier, db)}
        )
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": str(err)}
        )
    except SQLAlchemyError as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Database failure", "info": str(err)}
        )


def delete_clients_action(identify: IdentifierEntitySchema, db: Session):
    try:
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail={"message": delete_clients_persistence(identify, db)}
        )
    except ValueError as valErr:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": str(valErr)}
        )
    except SQLAlchemyError as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Database failure", "info": str(err)}
        )
