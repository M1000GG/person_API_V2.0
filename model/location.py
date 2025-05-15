from pydantic import BaseModel

class Location(BaseModel):
    code: int
    description: str