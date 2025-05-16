from typing import Optional
from pydantic import BaseModel


class ClientsSchema(BaseModel):
    idclient : Optional[int] = None
    clientname : str
    clientlastname : str
    clientphone : str
    clientemail : str
    clientaddress : str
    clientstatus : bool
    idtypeclient : int
    idriskclient : int
    idguarantorclient : Optional[int] = None
    iselegible : bool
