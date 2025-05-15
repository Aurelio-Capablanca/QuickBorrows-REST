from fastapi import FastAPI
#from .database import engine, Base
from application.apis.controllers import authentication_routes

app = FastAPI()

app.include_router(authentication_routes.router)