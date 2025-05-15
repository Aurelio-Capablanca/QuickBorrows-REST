from fastapi import FastAPI
from fastapi import FastAPI
#from .database import engine, Base

from application.apis.controllers import router as auth_router

app = FastAPI()

app.include_router(auth_router)