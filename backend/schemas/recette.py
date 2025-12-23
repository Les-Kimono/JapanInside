from typing import Optional
from pydantic import BaseModel, ConfigDict


class RecetteBase(BaseModel):
    nom: str
    description: Optional[str] = None
    ingredients: Optional[str] = None


class RecetteCreate(RecetteBase):
    pass


class RecetteOut(RecetteBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
