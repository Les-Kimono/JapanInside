from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from utils.get_db import get_db
import schemas
import crud
from models import Ville as VilleModel, Attraction as AttractionModel, Recette as RecetteModel
router = APIRouter()

@router.get("/villes", response_model=List[schemas.VilleOut])
def get_all_villes(db: Session = Depends(get_db)):
    """Return all villes ordered by position."""
    return crud.get_villes(db)


@router.get("/villes/{nom_ville}", response_model=schemas.VilleOut)
def get_ville(nom_ville: str, db: Session = Depends(get_db)):
    """Return a ville with its attractions and recettes."""
    villes = crud.get_villes(db)
    ville = next((v for v in villes if v.nom.lower() == nom_ville.lower()), None)
    if not ville:
        raise HTTPException(status_code=404, detail=f"Ville '{nom_ville}' non trouvée")
    return ville


@router.post("/villes", response_model=schemas.VilleOut)
def create_ville(ville: schemas.VilleCreate, db: Session = Depends(get_db)):
    """Create a new ville, including attractions and recettes."""
    db_ville = crud.create_ville(db, ville)

    for attraction in ville.attractions or []:
        db_ville.attractions.append(crud.create_attraction(db, attraction))

    for recette in ville.recettes or []:
        db_ville.recettes.append(crud.create_recette(db, recette))

    db.commit()
    db.refresh(db_ville)
    return db_ville



@router.put("/villes/reorder")
def reorder_villes(new_order: list[schemas.VilleOrder] = Body(...), db: Session = Depends(get_db)):
    """Update the order of villes according to client input."""
    for item in new_order:
        db_ville = crud.get_ville(db, item.id)
        if db_ville:
            db_ville.position = item.position # type : ignore
    db.commit()
    return {"message": "OK"}

@router.put("/villes/{id}", response_model=schemas.VilleOut)
def update_ville(
    id: int, ville_data: schemas.VilleCreate, db: Session = Depends(get_db)
):
    """Update an existing ville, including attractions and recettes."""
    ville: Optional[VilleModel] = (
        db.query(VilleModel).filter(VilleModel.id == id).first()
    )
    if ville is None:
        raise HTTPException(status_code=404, detail="Ville non trouvée")

    ville.nom = ville_data.nom  # type: ignore
    ville.position = ville_data.position  # type: ignore
    ville.description = ville_data.description  # type: ignore
    ville.latitude = ville_data.latitude  # type: ignore
    ville.longitude = ville_data.longitude  # type: ignore
    ville.population = ville_data.population  # type: ignore
    ville.meilleure_saison = ville_data.meilleure_saison  # type: ignore
    ville.climat = ville_data.climat  # type: ignore

    for attr in list(ville.attractions):
        db.delete(attr)
    ville.attractions.clear()

    for rec in list(ville.recettes):
        db.delete(rec)
    ville.recettes.clear()

    db.commit()

    if ville_data.attractions:
        for attraction in ville_data.attractions:
            ville.attractions.append(AttractionModel(**attraction.dict()))

    if ville_data.recettes:
        for recette in ville_data.recettes:
            db_recette = RecetteModel(**recette.dict())
            db.add(db_recette)
            ville.recettes.append(db_recette)

    db.commit()
    db.refresh(ville)
    return ville




@router.delete("/villes/{id}")
def delete_ville(id: int, db: Session = Depends(get_db)):
    """Delete a ville by ID."""
    success = crud.delete_ville(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Ville non trouvée")
    return {"message": "Ville supprimée avec succès"}
