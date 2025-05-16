from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from application.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain:str, hashed: str):
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
