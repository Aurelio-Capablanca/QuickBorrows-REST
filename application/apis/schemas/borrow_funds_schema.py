from typing import Optional
from pydantic import BaseModel


class BorrowFundsSchema(BaseModel):
    idfound: Optional[int] = None
    amountfound: float
    isinput: bool
