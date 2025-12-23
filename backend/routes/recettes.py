from fastapi import APIRouter

from sqlalchemy.orm import Session
from fastapi import Depends
import crud
import schemas

from utils.get_db import get_db
router = APIRouter()




@router.get("/recettes", response_model=list[schemas.RecetteOut])
def read_recettes(db: Session = Depends(get_db)):
    """Return all recettes."""
    return crud.get_recettes(db)


@router.post("/recettes", response_model=schemas.RecetteOut)
def create_recette(
    recette: schemas.RecetteCreate, db: Session = Depends(get_db)
):
    """Create a new recette."""
    return crud.create_recette(db, recette)
