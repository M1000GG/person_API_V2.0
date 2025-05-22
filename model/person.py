from pydantic import BaseModel
from model.location import Location
from model.typedoc import Typedoc

class Person(BaseModel):
    id: str
    name: str
    lastname: str
    age: int
    gender: str
    typedoc: Typedoc
    location: Location

class PersonCreate(BaseModel):
    id: str
    name: str
    lastname: str
    age: int
    gender: str
    typedoc_code: int
    location_code: int

class PersonUpdate(BaseModel):
    name: str
    lastname: str
    age: int
    gender: str
    typedoc_code: int
    location_code: int