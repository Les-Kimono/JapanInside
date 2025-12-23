from typing import List, Optional
from sqlalchemy.orm import Session
from models import Attraction as AttractionModel
import schemas

def create_attraction(db: Session, attraction: schemas.AttractionCreate) -> AttractionModel:
    db_attraction = AttractionModel(**attraction.dict())
    db.add(db_attraction)
    db.commit()
    db.refresh(db_attraction)
    return db_attraction

def get_attractions(db: Session, ville_id: Optional[int] = None) -> List[AttractionModel]:
    query = db.query(AttractionModel)
    if ville_id:
        query = query.filter(AttractionModel.ville_id == ville_id)
    return query.all()

def get_attraction(db: Session, attraction_id: int) -> Optional[AttractionModel]:
    return db.query(AttractionModel).filter(AttractionModel.id == attraction_id).first()

def update_attraction(db: Session, attraction_id: int, attraction_data: schemas.AttractionCreate) -> Optional[AttractionModel]:
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
