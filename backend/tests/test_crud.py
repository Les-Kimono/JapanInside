import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import crud
import models
import schemas
from utils.database import Base


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture(scope="function")
def db():
    """Crée une base de données propre pour chaque test."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_ville(db):
    """Ville de test."""
    ville = models.Ville(
        nom="Tokyo",
        position=1,
        description="Capitale du Japon",
        latitude=35.6895,
        longitude=139.6917,
        population=14000000,
        meilleure_saison="Printemps",
        climat="Tempéré",
    )
    db.add(ville)
    db.commit()
    db.refresh(ville)
    return ville


@pytest.fixture
def sample_attractions(db, sample_ville):
    attractions = [
        models.Attraction(nom="Tokyo Tower", description="Tour emblématique", ville_id=sample_ville.id),
        models.Attraction(nom="Senso-ji", description="Temple historique", ville_id=sample_ville.id),
    ]
    db.add_all(attractions)
    db.commit()
    return attractions


@pytest.fixture
def sample_recettes(db):
    recettes = [
        models.Recette(nom="Ramen", description="Soupe japonaise", ingredients="Nouilles, bouillon"),
        models.Recette(nom="Sushi", description="Riz vinaigré", ingredients="Riz, poisson"),
    ]
    db.add_all(recettes)
    db.commit()
    return recettes


# ---------- VILLE ----------

def test_create_ville(db):
    ville_data = schemas.VilleCreate(
        nom="Kyoto", position=2, description="Ancienne capitale",
        latitude=35.0116, longitude=135.7681, population=1500000,
        meilleure_saison="Printemps", climat="Tempéré"
    )
    ville = crud.create_ville(db, ville_data)
    assert ville.id is not None
    assert ville.nom == "Kyoto"

def test_get_villes(db, sample_ville):
    villes = crud.get_villes(db)
    assert len(villes) == 1
    assert villes[0].nom == "Tokyo"

def test_get_ville(db, sample_ville):
    ville = crud.get_ville(db, sample_ville.id)
    assert ville.nom == "Tokyo"
    assert crud.get_ville(db, 9999) is None 

def test_update_ville(db, sample_ville):
    update_data = schemas.VilleCreate(
        nom="Tokyo Updated", position=1, description="Capitale modifiée",
        latitude=35.6895, longitude=139.6917, population=14000000,
        meilleure_saison="Été", climat="Tempéré"
    )
    ville = crud.update_ville(db, sample_ville.id, update_data)
    assert ville.nom == "Tokyo Updated"
    assert ville.meilleure_saison == "Été"

    assert crud.update_ville(db, 9999, update_data) is None

def test_delete_ville(db, sample_ville):
    success = crud.delete_ville(db, sample_ville.id)
    assert success
    assert crud.get_ville(db, sample_ville.id) is None

    assert crud.delete_ville(db, 9999) is False


# ---------- ATTRACTION ----------

def test_create_attraction(db, sample_ville):
    attraction_data = schemas.AttractionCreate(
        nom="Meiji Shrine", description="Sanctuaire célèbre", ville_id=sample_ville.id
    )
    attraction = crud.create_attraction(db, attraction_data)
    assert attraction.id is not None
    assert attraction.nom == "Meiji Shrine"

def test_get_attractions(db, sample_attractions):
    attractions = crud.get_attractions(db)
    assert len(attractions) == 2

    filtered = crud.get_attractions(db, ville_id=sample_attractions[0].ville_id)
    assert len(filtered) == 2

def test_get_attraction(db, sample_attractions):
    attr = crud.get_attraction(db, sample_attractions[0].id)
    assert attr.nom == "Tokyo Tower"
    assert crud.get_attraction(db, 9999) is None

def test_update_attraction(db, sample_attractions):
    update_data = schemas.AttractionCreate(
        nom="Tokyo Tower Updated", description="Tour modifiée", ville_id=sample_attractions[0].ville_id
    )
    attr = crud.update_attraction(db, sample_attractions[0].id, update_data)
    assert attr.nom == "Tokyo Tower Updated"
    assert crud.update_attraction(db, 9999, update_data) is None

def test_delete_attraction(db, sample_attractions):
    success = crud.delete_attraction(db, sample_attractions[0].id)
    assert success
    assert crud.get_attraction(db, sample_attractions[0].id) is None
    assert crud.delete_attraction(db, 9999) is False


# ---------- RECETTE ----------

def test_create_recette(db):
    recette_data = schemas.RecetteCreate(
        nom="Okonomiyaki", description="Crêpe japonaise", ingredients="Chou, pâte"
    )
    recette = crud.create_recette(db, recette_data)
    assert recette.id is not None
    assert recette.nom == "Okonomiyaki"

def test_create_recette_with_ville(db, sample_ville):
    recette_data = schemas.RecetteCreate(nom="Takoyaki", description="Boulettes de poulpe", ingredients="Poulpe, pâte")
    recette = crud.create_recette(db, recette_data, ville_ids=[sample_ville.id])
    assert recette.id is not None
    assert recette.villes[0].nom == "Tokyo"

def test_get_recettes(db, sample_recettes):
    recettes = crud.get_recettes(db)
    assert len(recettes) == 2

    filtered = crud.get_recettes(db, ville_id=1)
    assert filtered == []

def test_get_recette(db, sample_recettes):
    recette = crud.get_recette(db, sample_recettes[0].id)
    assert recette.nom == "Ramen"
    assert crud.get_recette(db, 9999) is None

def test_update_recette(db, sample_recettes, sample_ville):
    update_data = schemas.RecetteCreate(nom="Ramen Updated", description="Nouvelle soupe", ingredients="Nouilles, bouillon")
    recette = crud.update_recette(db, sample_recettes[0].id, update_data, ville_ids=[sample_ville.id])
    assert recette.nom == "Ramen Updated"
    assert recette.villes[0].nom == "Tokyo"
    assert crud.update_recette(db, 9999, update_data) is None

def test_delete_recette(db, sample_recettes):
    success = crud.delete_recette(db, sample_recettes[0].id)
    assert success
    assert crud.get_recette(db, sample_recettes[0].id) is None
    assert crud.delete_recette(db, 9999) is False
