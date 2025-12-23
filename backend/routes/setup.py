


from fastapi import APIRouter

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from utils.database import Base, engine

import utils.create_tables as create_tables
import utils.insert_data as insert_data
from utils.get_db import get_db
router = APIRouter()



@router.post("/createDB")
def setup():
    """Create all database tables."""
    create_tables.execute()
    return {}, 200


@router.post("/flushDB")
def flush_db(db: Session = Depends(get_db)):
    """Drop and recreate all database tables."""
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
def insert():
    """
    Insert initial villes, attractions.

    And recettes data into the database.
    """
    insert_data.execute()
    return {}, 200