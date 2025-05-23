from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AdministratorSchema(BaseModel):
    idadministrator: Optional[int] = None
    adminname: str
    adminlastname: str
    adminemail: str
    adminpass: str
    adminphone: Optional[str] = None
    adminstatus: bool
    datecreated: Optional[datetime] = None
