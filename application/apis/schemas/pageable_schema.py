from typing import Optional
from pydantic import BaseModel

class PageableSchema(BaseModel):
    page:  Optional[int] = 0
    limit: Optional[int] = 10