from fastapi import FastAPI
#from .database import engine, Base
from application.apis.controllers import authentication_controller, test_endpoints, admin_controller, client_controller, borrow_controller, borrow_funds_controller

app = FastAPI()

app.include_router(authentication_controller.router)
app.include_router(admin_controller.router)
app.include_router(client_controller.router)
app.include_router(borrow_controller.router)
app.include_router(borrow_funds_controller.router)