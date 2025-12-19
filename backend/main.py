from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import joinedload
from fastapi.staticfiles import StaticFiles
import json

with open("villes.json", "r", encoding="utf-8") as f:
    villes_data = json.load(f)
  
itineraire = ["Tokyo", "Hakone", "Kyoto", "Nara", "Osaka", "Hiroshima", "Tokyo"]

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Japan Inside API")
app.mount("/static", StaticFiles(directory="utils"), name="static")
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/api/hello')
def hello_world():
    return {"message": "Hello World"}

@app.get('/')
def hello_world():
    DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///:memory:"
)
    print(DATABASE_URL)
    return {}, 200



# API pour les données des villes
@app.get("/api/villes", response_model=list[schemas.Ville])
async def get_all_villes(db: Session = Depends(get_db)):
    """Retourne toutes les villes disponibles"""
    return crud.get_villes(db)


@app.post("/api/villes", response_model=schemas.Ville)

def create_ville(
     ville: schemas.VilleCreate,       
    db: Session = Depends(get_db) 
):
    db_ville = models.Ville(
        nom=ville.nom,
        position=ville.position,
        description=ville.description,
        latitude=ville.latitude,
        longitude=ville.longitude,
        population=ville.population,
        meilleure_saison=ville.meilleure_saison,
        informations_supp=ville.informations_supp
    )
    db.add(db_ville)
    db.commit()
    db.refresh(db_ville)

    for attraction in ville.attractions:
        db_ville.attractions.append(models.Attraction(**attraction.dict()))

    for recette in ville.recettes:
        db_recette = models.Recette(**recette.dict())
        db.add(db_recette)
        db_ville.recettes.append(db_recette)

    db.commit()
    db.refresh(db_ville)
    return db_ville
@app.get("/api/villes/{nom_ville}", response_model=schemas.VilleOut)
def get_ville(nom_ville: str, db: Session = Depends(get_db)):
    ville = (
        db.query(models.Ville)
        .options(joinedload(models.Ville.attractions), joinedload(models.Ville.recettes))
        .filter(models.Ville.nom.ilike(nom_ville))
        .first()
    )
    if not ville:
        raise HTTPException(status_code=404, detail=f"Ville '{nom_ville}' non trouvée")
    return ville

@app.get("/api/itineraire")
async def get_itineraire_complet():
    """Retourne l'itinéraire complet"""
    return {
        "itineraire": itineraire,
        "etapes": [
            {
                "ordre": i+1,
                "ville": ville,
                "coords": [villes_data[ville]["latitude"], villes_data[ville]["longitude"]]
            }
            for i, ville in enumerate(itineraire[:-1])  # Exclure le dernier Tokyo
        ]
    }

# Routes existantes de votre API
@app.get('/api/hello')
def hello_world():
    return {"message": "Bienvenue sur Japan Inside API!"}


@app.get("/api/recettes", response_model=list[schemas.Recette])
def read_recettes(db: Session = Depends(get_db)):
    """Retourne toutes les recettes"""
    return crud.get_recettes(db)

@app.post("/api/recettes", response_model=schemas.Recette)
def create_recette(recette: schemas.RecetteCreate, db: Session = Depends(get_db)):
    """Crée une nouvelle recette"""
    return crud.create_recette(db, recette)

# Route de santé de l'API
@app.get("/health")
async def health_check():
    """Vérifie l'état de l'API"""
    return {
        "status": "healthy",
        "service": "Japan Inside API",
        "version": "1.0.0",
        "endpoints": {
            "carte": "/carte",
            "villes": "/api/villes",
            "itineraire": "/api/itineraire",
            "articles": "/api/articles",
            "recettes": "/api/recettes"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
