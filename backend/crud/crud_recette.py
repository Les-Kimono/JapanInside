from typing import List, Optional
from sqlalchemy.orm import Session
from models import Recette as RecetteModel, Ville as VilleModel
import schemas

def create_recette(db: Session, recette: schemas.RecetteCreate, ville_ids: Optional[List[int]] = None) -> RecetteModel:
    db_recette = RecetteModel(**recette.dict())
    db.add(db_recette)
    db.commit()
    db.refresh(db_recette)

    if ville_ids:
        villes = db.query(VilleModel).filter(VilleModel.id.in_(ville_ids)).all()
        for ville in villes:
            ville.recettes.append(db_recette)
        db.commit()

    return db_recette

def get_recettes(db: Session, ville_id: Optional[int] = None) -> List[RecetteModel]:
    query = db.query(RecetteModel)
    if ville_id:
        query = query.join(VilleModel.recettes).filter(VilleModel.id == ville_id)
    return query.all()

def get_recette(db: Session, recette_id: int) -> Optional[RecetteModel]:
    return db.query(RecetteModel).filter(RecetteModel.id == recette_id).first()

def update_recette(db: Session, recette_id: int, recette_data: schemas.RecetteCreate, ville_ids: Optional[List[int]] = None) -> Optional[RecetteModel]:
    db_recette = get_recette(db, recette_id)
    if db_recette:
        for key, value in recette_data.dict(exclude_unset=True).items():
            setattr(db_recette, key, value)
        if ville_ids is not None:
            db_recette.villes = db.query(VilleModel).filter(VilleModel.id.in_(ville_ids)).all()
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
