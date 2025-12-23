from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from models import Ville as VilleModel
import schemas

def create_ville(db: Session, ville: schemas.VilleCreate) -> VilleModel:
    db_ville = VilleModel(**ville.dict())
    db.add(db_ville)
    db.commit()
    db.refresh(db_ville)
    return db_ville

def get_villes(db: Session, limit: int = 100) -> List[VilleModel]:
    return (
        db.query(VilleModel)
        .options(joinedload(VilleModel.attractions), joinedload(VilleModel.recettes))
        .order_by(VilleModel.position.asc())
        .limit(limit)
        .all()
    )

def get_ville(db: Session, ville_id: int) -> Optional[VilleModel]:
    return db.query(VilleModel).filter(VilleModel.id == ville_id).first()

def update_ville(db: Session, ville_id: int, ville_data: schemas.VilleCreate) -> Optional[VilleModel]:
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
