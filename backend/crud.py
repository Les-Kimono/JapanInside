from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
import models, schemas

# ---------- Villes ----------

def create_ville(db: Session, ville: schemas.VilleCreate) -> models.Ville:
    db_ville = models.Ville(**ville.dict())
    db.add(db_ville)
    db.commit()
    db.refresh(db_ville)
    return db_ville

def get_villes(db: Session, skip: int = 0, limit: int = 100) -> List[models.Ville]:
    return (
        db.query(models.Ville)
        .options(
            joinedload(models.Ville.attractions), 
            joinedload(models.Ville.recettes)      
        )
        .offset(skip)
        .limit(limit)
        .all()
    )
def get_ville(db: Session, ville_id: int) -> Optional[models.Ville]:
    return db.query(models.Ville).filter(models.Ville.id == ville_id).first()

def update_ville(db: Session, ville_id: int, ville_data: schemas.VilleCreate) -> Optional[models.Ville]:
    db_ville = get_ville(db, ville_id)
    if db_ville:
        for key, value in ville_data.dict(exclude_unset=True).items():
            setattr(db_ville, key, value)
        db.commit()
        db.refresh(db_ville)
    return db_ville

def delete_ville(db: Session, ville_id: int) -> bool:
    db_ville = get_ville(db, ville_id)
    if db_ville:
        db.delete(db_ville)
        db.commit()
        return True
    return False

# ---------- Attractions ----------

def create_attraction(db: Session, attraction: schemas.AttractionCreate) -> models.Attraction:
    db_attraction = models.Attraction(**attraction.dict())
    db.add(db_attraction)
    db.commit()
    db.refresh(db_attraction)
    return db_attraction

def get_attractions(db: Session, ville_id: Optional[int] = None) -> List[models.Attraction]:
    query = db.query(models.Attraction)
    if ville_id is not None:
        query = query.filter(models.Attraction.ville_id == ville_id)
    return query.all()

def get_attraction(db: Session, attraction_id: int) -> Optional[models.Attraction]:
    return db.query(models.Attraction).filter(models.Attraction.id == attraction_id).first()

def update_attraction(db: Session, attraction_id: int, attraction_data: schemas.AttractionCreate) -> Optional[models.Attraction]:
    db_attraction = get_attraction(db, attraction_id)
    if db_attraction:
        for key, value in attraction_data.dict(exclude_unset=True).items():
            setattr(db_attraction, key, value)
        db.commit()
        db.refresh(db_attraction)
    return db_attraction

def delete_attraction(db: Session, attraction_id: int) -> bool:
    db_attraction = get_attraction(db, attraction_id)
    if db_attraction:
        db.delete(db_attraction)
        db.commit()
        return True
    return False

# ---------- Recettes ----------

def create_recette(db: Session, recette: schemas.RecetteCreate, ville_ids: Optional[List[int]] = None) -> models.Recette:
    db_recette = models.Recette(**recette.dict())
    db.add(db_recette)
    db.commit()
    db.refresh(db_recette)

    if ville_ids:
        villes = db.query(models.Ville).filter(models.Ville.id.in_(ville_ids)).all()
        for ville in villes:
            ville.recettes.append(db_recette)
        db.commit()
    
    return db_recette

def get_recettes(db: Session, ville_id: Optional[int] = None) -> List[models.Recette]:
    query = db.query(models.Recette)
    if ville_id is not None:
        query = query.join(models.Ville.recettes).filter(models.Ville.id == ville_id)
    return query.all()

def get_recette(db: Session, recette_id: int) -> Optional[models.Recette]:
    return db.query(models.Recette).filter(models.Recette.id == recette_id).first()

def update_recette(db: Session, recette_id: int, recette_data: schemas.RecetteCreate, ville_ids: Optional[List[int]] = None) -> Optional[models.Recette]:
    db_recette = get_recette(db, recette_id)
    if db_recette:
        for key, value in recette_data.dict(exclude_unset=True).items():
            setattr(db_recette, key, value)
        if ville_ids is not None:
            db_recette.villes = db.query(models.Ville).filter(models.Ville.id.in_(ville_ids)).all()
        db.commit()
        db.refresh(db_recette)
    return db_recette

def delete_recette(db: Session, recette_id: int) -> bool:
    db_recette = get_recette(db, recette_id)
    if db_recette:
        db.delete(db_recette)
        db.commit()
        return True
    return False
