from models.city import City
from pydantic import BaseModel, constr


class CityCreateSchema(BaseModel):
    name: constr(min_length=1, max_length=100)
    description: constr(max_length=255) | None = None


class CityReadSchema(BaseModel):
    id: int
    name: str
    description: str | None = None

    class Config:
        from_attributes = True
