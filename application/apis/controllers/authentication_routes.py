from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from application.authentication.schemas import Token, LoginInput
from application.apis.businesslogic.authactions import authenticate
from application.database.session import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/login", response_model=Token)
def login(payload: LoginInput, db: Session = Depends(get_db)):
    return authenticate(form_data=payload, db=db)
