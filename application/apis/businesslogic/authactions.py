from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from application.apis.services.adminservices import get_admins_by_email
from application.core.security import verify_password, create_access_token



def authenticate(form_data: OAuth2PasswordRequestForm, db: Session):
    user = get_admins_by_email(form_data.username, db)
    if not user or not verify_password(form_data.password, user.adminpass):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.adminemail})
    return {"access_token": access_token, "token_type": "bearer"}