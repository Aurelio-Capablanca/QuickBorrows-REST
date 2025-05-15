from fastapi import APIRouter, Depends
from application.authentication.jwtdependency import get_current_user, oauth2_scheme

router = APIRouter()

@router.get("/debug-token")
def debug_token(token: str = Depends(oauth2_scheme)):
    print(f"Token received: {token}")
    return {"token": token}

@router.get("/secured-hi")
def secured_hi(current_user=Depends(get_current_user)):
    return {"message": f"Hi {current_user.adminname}, you're authenticated!"}