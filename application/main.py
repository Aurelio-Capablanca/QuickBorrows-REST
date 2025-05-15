from fastapi import FastAPI
#from .database import engine, Base
from application.apis.controllers import authentication_routes
from application.apis.controllers import testendpoints

app = FastAPI()

app.include_router(authentication_routes.router)
app.include_router(testendpoints.router)