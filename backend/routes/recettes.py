from fastapi import APIRouter

from sqlalchemy.orm import Session
from fastapi import Depends, Request, status, HTTPException
import crud
import schemas

from utils.get_db import get_db
from utils.login_utils import check_login
router = APIRouter()




@router.get("/recettes", response_model=list[schemas.RecetteOut])
def read_recettes(db: Session = Depends(get_db)):
    """Return all recettes."""
    return crud.get_recettes(db)


@router.post("/recettes", response_model=schemas.RecetteOut)
def create_recette(
    request: Request, recette: schemas.RecetteCreate, db: Session = Depends(get_db)
):
    """Create a new recette."""
    if not check_login(request):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )
    return crud.create_recette(db, recette)
