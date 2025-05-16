from fastapi import HTTPException
from sqlalchemy.orm import Session

from application.apis.persistence.adminpersistence import get_admins_by_email
from application.authentication.schemas import LoginInput
from application.core.security import verify_password, create_access_token



def authenticate(form_data: LoginInput, db: Session):
    user = get_admins_by_email(form_data.username, db)
    if not user or not verify_password(form_data.password, user.adminpass):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.adminemail})
    return {"access_token": access_token, "token_type": "bearer"}