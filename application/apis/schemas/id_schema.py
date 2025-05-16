from pydantic import BaseModel

class IdentifierEntitySchema(BaseModel):
    identity: int