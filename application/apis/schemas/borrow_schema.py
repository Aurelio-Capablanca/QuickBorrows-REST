from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class BillConditions(BaseModel):
    numpayments : list[int]
    paymentsof: list[float]
    generatetofill: bool


class BorrowSchema(BaseModel):
    idborrow: Optional[int] = None
    borrowamount: float
    percentagetax: Optional[float] = None
    datetaken: Optional[datetime] = None
    duedate: datetime
    idmethod: int
    idclient: int
    idfound: int


class BorrowRequest(BaseModel):
    borrow:BorrowSchema
    billconditions:BillConditions