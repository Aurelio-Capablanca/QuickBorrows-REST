from typing import Optional
from pydantic import BaseModel


class Clients(BaseModel):
    idclient : Optional[int] = None
    clientName : str
    clientLastname : str
    clientPhone : str
    clientEmail : str
    clientAddress : str
    clientStatus : bool
    idTypeClient : int
    idRiskClient : int
    idGuarantorClient : int
    isElegible : bool
