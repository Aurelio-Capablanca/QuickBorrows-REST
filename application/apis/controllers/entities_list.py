from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from starlette import status

from application.apis.models.payment_methods_model import PaymentMethods
from application.apis.models.risk_levels_model import RiskLevels
from application.apis.models.type_client_model import TypeClient
from application.authentication.jwt_dependency import get_current_user
from application.database.session import get_db

router = APIRouter()


@router.get("/api/get-payment-methods")
def get_payment_methods(db: Session = Depends(get_db),
                            current_user=Depends(get_current_user)):
    try:
        get_all_methods = db.query(PaymentMethods).all()
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail={"message": "Success", "data": get_all_methods}
        )
    except SQLAlchemyError as se:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Database failure", "info": str(se)}
        )

@router.get("/api/get-risk-levels")
def get_risk_levels(db: Session = Depends(get_db),
                            current_user=Depends(get_current_user)):
    try:
        get_all_risk_levels = db.query(RiskLevels).all()
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail={"message": "Success", "data": get_all_risk_levels}
        )
    except SQLAlchemyError as se:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Database failure", "info": str(se)}
        )

@router.get("/api/get-type-clients")
def get_risk_levels(db: Session = Depends(get_db),
                            current_user=Depends(get_current_user)):
    try:
        get_all_type_clients = db.query(TypeClient).all()
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail={"message": "Success", "data": get_all_type_clients}
        )
    except SQLAlchemyError as se:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Database failure", "info": str(se)}
        )