


from fastapi import APIRouter

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Request, status

from utils.database import Base, engine

import utils.create_tables as create_tables
import utils.insert_data as insert_data
from utils.get_db import get_db
from utils.login_utils import check_login
router = APIRouter()



@router.post("/createDB")
def setup(request: Request):
    """Create all database tables."""
    if not check_login(request):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )
    create_tables.execute()
    return {}, 200


@router.post("/flushDB")
def flush_db(request: Request, db: Session = Depends(get_db)):
    """Drop and recreate all database tables."""
    if not check_login(request):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )
    try:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        return {}, 200
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la réinitialisation : {str(e)}",
        )

@router.post("/insertDATA")
def insert(request: Request):
    """
    Insert initial villes, attractions.

    And recettes data into the database.
    """
    if not check_login(request):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )
    insert_data.execute()
    return {}, 200