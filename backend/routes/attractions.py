from fastapi import APIRouter

from sqlalchemy.orm import Session
from fastapi import Depends
from utils.database import SessionLocal
import crud
import schemas

from utils.get_db import get_db
router = APIRouter()

@router.get("/attractions", response_model=list[schemas.AttractionOut])
async def get_all_attractions(db: Session = Depends(get_db)):
    """Return all attractions."""
    return crud.get_attractions(db)
