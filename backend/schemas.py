from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class VilleBase(BaseModel):
    nom: str
    position: Optional[int] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    population: Optional[int] = None
    meilleure_saison: Optional[str] = None
    informations_supp: Optional[Dict[str, Any]] = None



class Ville(VilleBase):
    id: int
    model_config = {"from_attributes": True}


class AttractionBase(BaseModel):
    nom: str
    description: Optional[str] = None
    ville_id: int

class Attraction(AttractionBase):
    id: int
    model_config = {"from_attributes": True}

class RecetteBase(BaseModel):
    nom: str
    description: Optional[str] = None
    ingredients: Optional[str] = None

class Recette(RecetteBase):
    id: int
    model_config = {"from_attributes": True}



class AttractionCreate(BaseModel):
    nom: str
    description: Optional[str] = None

class RecetteCreate(BaseModel):
    nom: str
    description: Optional[str] = None
    ingredients: Optional[str] = None

class VilleCreate(BaseModel):
    nom: str
    position: Optional[int] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    population: Optional[int] = None
    meilleure_saison: Optional[str] = None
    informations_supp: Optional[Dict[str, Any]] = None

    attractions: Optional[List[AttractionCreate]] = []
    recettes: Optional[List[RecetteCreate]] = []




class AttractionOut(BaseModel):
    id: int
    nom: str
    description: Optional[str]
    class Config:
        orm_mode = True

class RecetteOut(BaseModel):
    id: int
    nom: str
    description: Optional[str]
    ingredients: Optional[str]
    class Config:
        orm_mode = True

class VilleOut(BaseModel):
    id: int
    nom: str
    position: Optional[int]
    description: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    population: Optional[int]
    meilleure_saison: Optional[str]
    informations_supp: Optional[Dict[str, Any]] = None
    attractions: List[AttractionOut] = []
    recettes: List[RecetteOut] = []
    class Config:
        orm_mode = True