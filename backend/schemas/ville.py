from typing import List, Optional
from pydantic import BaseModel, ConfigDict

from schemas.attraction import AttractionCreate, AttractionOut
from schemas.recette import RecetteCreate, RecetteOut


class VilleBase(BaseModel):
    nom: str
    position: Optional[int] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    population: Optional[int] = None
    meilleure_saison: Optional[str] = None
    climat: Optional[str] = None


class VilleCreate(VilleBase):
    attractions: Optional[List[AttractionCreate]] = []
    recettes: Optional[List[RecetteCreate]] = []


class VilleOut(VilleBase):
    id: int
    attractions: List[AttractionOut] = []
    recettes: List[RecetteOut] = []

    model_config = ConfigDict(from_attributes=True)

class VilleOrder(BaseModel):
    id: int
    position: int
