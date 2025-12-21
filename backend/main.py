"""Main FastAPI application for Japan Inside API.

Provides endpoints for villes, attractions, recettes, and database management.
"""

import json
import os

import create_tables
import crud
import insert_data
import models
import schemas
from database import Base, SessionLocal, engine
from fastapi import Body, Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload
from types import Optional

# Load villes data from JSON
with open("villes.json", "r", encoding="utf-8") as f:
    villes_data = json.load(f)

itineraire = [
    "Tokyo",
    "Hakone",
    "Kyoto",
    "Nara",
    "Osaka",
    "Hiroshima",
    "Tokyo",
]

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Japan Inside API")
origins = ["http://localhost:5173", "http://127.0.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    """Provide a database session to FastAPI routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def hello_world():
    """Return a simple status response."""
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")
    print(DATABASE_URL)
    return {}, 200


@app.get("/api/villes", response_model=list[schemas.VilleOut])
async def get_all_villes(db: Session = Depends(get_db)):
    """Return all villes ordered by position."""
    return db.query(models.Ville).order_by(models.Ville.position).all()


@app.get("/api/attractions", response_model=list[schemas.AttractionOut])
async def get_all_attractions(db: Session = Depends(get_db)):
    """Return all attractions."""
    return crud.get_attractions(db)


@app.put("/api/villes/reorder")
def reorder_villes(
    new_order: list[schemas.VilleOrder] = Body(...),
    db: Session = Depends(get_db),
):
    """Update the order of villes according to client input."""
    for item in new_order:
        ville: Optional[models.Ville] = (
            db.query(models.Ville).filter(models.Ville.id == item.id).first()
        )
        if ville:
            ville.position = item.position
    db.commit()
    return {"message": "OK"}


@app.put("/api/villes/{id}", response_model=schemas.VilleOut)
def update_ville(
    id: int, ville_data: schemas.VilleCreate, db: Session = Depends(get_db)
):
    """Update an existing ville, including its attractions and recettes."""
    ville = db.query(models.Ville).filter(models.Ville.id == id).first()
    if not ville:
        raise HTTPException(status_code=404, detail="Ville non trouvée")

    # Update fields
    ville.nom = ville_data.nom
    ville.position = ville_data.position
    ville.description = ville_data.description
    ville.latitude = ville_data.latitude
    ville.longitude = ville_data.longitude
    ville.population = ville_data.population
    ville.meilleure_saison = ville_data.meilleure_saison
    ville.climat = ville_data.climat

    # Remove old attractions and recettes
    for attr in list(ville.attractions):
        db.delete(attr)
    ville.attractions.clear()

    for rec in list(ville.recettes):
        db.delete(rec)
    ville.recettes.clear()

    db.commit()

    # Add new attractions (only if not None)
    if ville_data.attractions:
        for attraction in ville_data.attractions:
            ville.attractions.append(models.Attraction(**attraction.dict()))

    # Add new recettes (only if not None)
    if ville_data.recettes:
        for recette in ville_data.recettes:
            db_recette = models.Recette(**recette.dict())
            db.add(db_recette)
            ville.recettes.append(db_recette)

    db.commit()
    db.refresh(ville)
    return ville


@app.post("/api/villes", response_model=schemas.Ville)
def create_ville(ville: schemas.VilleCreate, db: Session = Depends(get_db)):
    """Create a new ville, including its attractions and recettes."""
    db_ville = models.Ville(
        nom=ville.nom,
        position=ville.position,
        description=ville.description,
        latitude=ville.latitude,
        longitude=ville.longitude,
        population=ville.population,
        meilleure_saison=ville.meilleure_saison,
        climat=ville.climat,
    )
    db.add(db_ville)
    db.commit()
    db.refresh(db_ville)

    if ville.attractions:
        for attraction in ville.attractions:
            db_ville.attractions.append(models.Attraction(**attraction.dict()))

    if ville.recettes:
        for recette in ville.recettes:
            db_recette = models.Recette(**recette.dict())
            db.add(db_recette)
            db_ville.recettes.append(db_recette)

    db.commit()
    db.refresh(db_ville)
    return db_ville


@app.post("/api/createDB")
def setup():
    """Create all database tables."""
    create_tables.execute()
    return {}, 200


@app.post("/api/flushDB")
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


@app.post("/api/insertDATA")
def insert():
    """
    Insert initial villes, attractions.

    And recettes data into the database.
    """
    insert_data.execute()
    return {}, 200


@app.get("/api/villes/{nom_ville}", response_model=schemas.VilleOut)
def get_ville(nom_ville: str, db: Session = Depends(get_db)):
    """Return a ville with its attractions and recettes."""
    ville = (
        db.query(models.Ville)
        .options(
            joinedload(models.Ville.attractions),
            joinedload(models.Ville.recettes),
        )
        .filter(models.Ville.nom.ilike(nom_ville))
        .first()
    )
    if not ville:
        raise HTTPException(
            status_code=404, detail=f"Ville '{nom_ville}' non trouvée"
        )
    return ville


@app.delete("/api/villes/{id}")
def delete_ville(id: int, db: Session = Depends(get_db)):
    """Delete a ville by ID."""
    ville = db.query(models.Ville).filter(models.Ville.id == id).first()
    if not ville:
        raise HTTPException(status_code=404, detail="Ville non trouvée")
    db.delete(ville)
    db.commit()


@app.get("/api/itineraire")
async def get_itineraire_complet():
    """Return the full itinerary with coordinates for each étape."""
    return {
        "itineraire": itineraire,
        "etapes": [
            {
                "ordre": i + 1,
                "ville": ville,
                "coords": [
                    villes_data[ville]["latitude"],
                    villes_data[ville]["longitude"],
                ],
            }
            for i, ville in enumerate(itineraire[:-1])
        ],
    }


@app.get("/api/recettes", response_model=list[schemas.Recette])
def read_recettes(db: Session = Depends(get_db)):
    """Return all recettes."""
    return crud.get_recettes(db)


@app.post("/api/recettes", response_model=schemas.Recette)
def create_recette(
    recette: schemas.RecetteCreate, db: Session = Depends(get_db)
):
    """Create a new recette."""
    return crud.create_recette(db, recette)


@app.get("/api/health", response_model=dict)
async def health_check():
    """Return the API health status."""
    return {
        "status": "healthy",
        "service": "Japan Inside API",
        "version": "1.0.0",
        "description": """Consulter les villes,
        attractions et recettes japonaises""",
        "endpoints": {
            "hello": "/api/hello",
            "villes": "/api/villes",
            "ville_detail": "/api/villes/{nom_ville}",
            "itineraire": "/api/itineraire",
            "recettes": "/api/recettes",
            "create_ville": "/api/villes [POST]",
            "create_recette": "/api/recettes [POST]",
            "flush_db": "/api/flushDB [POST]",
            "setup_db": "/api/createDB [POST]",
            "insert_data": "/api/insertDATA [POST]",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
