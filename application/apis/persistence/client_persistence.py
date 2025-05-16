from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from application.apis.schemas.id_schema import IdentifierEntitySchema
from application.apis.schemas.pageable_schema import PageableSchema
from application.apis.models.client_model import Clients


def delete_clients_persistence(identify: IdentifierEntitySchema, db: Session):
    client = db.query(Clients).filter(Clients.idclient == identify.identity)
    if not client:
        return "Client not Deleted"
    db.delete(client)
    db.commit()
    return "Client Deleted"


def get_clients_all_persistence(page: PageableSchema, db: Session):
    return db.query(Clients).offset(page.page).limit(page.limit).all()


def create_clients_persistence(client: Clients, db: Session):
    try:
        if client.idclient is None:
            db.add(client)
            db.commit()
            db.refresh(client)
            db.close()
            return "Client Created"
        client_get = db.query(Clients).filter(Clients.idclient == client.idclient).first()
        if not client_get:
            return ValueError("Client not Found")
        db.merge(client)
        db.commit()
        db.close()
        return "Client Updated"
    except SQLAlchemyError:
        db.rollback()
        return SQLAlchemyError("Database Operation Failed")
