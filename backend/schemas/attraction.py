from typing import Optional
from pydantic import BaseModel, ConfigDict


class AttractionBase(BaseModel):
    nom: str
    description: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    ville_id: int


class AttractionCreate(AttractionBase):
    pass


class AttractionOut(AttractionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
