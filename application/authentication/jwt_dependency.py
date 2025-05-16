from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from application.core.config import settings
from sqlalchemy.orm import Session
from application.database.session import get_db
from application.apis.models.admin_model import Administrators

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"Authorization": "Bearer"}, )
    try:

        payload = jwt.decode(token,
                             settings.secret_key,
                             algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError as e:
        print("JWT Decode Error:", str(e))
        raise credentials_exception
    user = db.query(Administrators).filter(Administrators.adminemail == email).first()
    if user is None:
        raise credentials_exception
    return user
