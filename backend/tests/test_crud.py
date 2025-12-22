import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import crud
import models
import schemas
from database import Base


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
    """
    Crée une base de données propre pour chaque test.
    """
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_ville(db):
    """
    Ville de test avec attractions.
    """
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
        models.Attraction(
            nom="Tokyo Tower",
            description="Tour emblématique",
            ville_id=sample_ville.id,
        ),
        models.Attraction(
            nom="Senso-ji",
            description="Temple historique",
            ville_id=sample_ville.id,
        ),
    ]
    db.add_all(attractions)
    db.commit()
    return attractions


@pytest.fixture
def sample_recettes(db):
    recettes = [
        models.Recette(
            nom="Ramen",
            description="Soupe japonaise",
            ingredients="Nouilles, bouillon"
        ),
        models.Recette(
            nom="Sushi",
            description="Riz vinaigré",
            ingredients="Riz, poisson"
        ),
    ]
    db.add_all(recettes)
    db.commit()
    return recettes



def test_get_attractions(db, sample_attractions):
    """
    Vérifie que toutes les attractions sont retournées.
    """
    attractions = crud.get_attractions(db)

    assert len(attractions) == 2
    noms = [a.nom for a in attractions]
    assert "Tokyo Tower" in noms
    assert "Senso-ji" in noms


def test_get_recettes(db, sample_recettes):
    """
    Vérifie la récupération des recettes.
    """
    recettes = crud.get_recettes(db)

    assert len(recettes) == 2
    assert recettes[0].nom == "Ramen"
    assert recettes[1].nom == "Sushi"


def test_create_recette(db):
    """
    Vérifie la création d'une recette.
    """
    recette_data = schemas.RecetteCreate(
        nom="Okonomiyaki",
        description="Crêpe japonaise",
        ingredients="Chou, pâte"
    )

    recette = crud.create_recette(db, recette_data)

    assert recette.id is not None
    assert recette.nom == "Okonomiyaki"
    assert recette.ingredients == "Chou, pâte"


def test_create_recette_persists_in_db(db):
    """
    Vérifie que la recette est bien persistée.
    """
    recette_data = schemas.RecetteCreate(
        nom="Takoyaki",
        description="Boulettes de poulpe",
        ingredients="Poulpe, pâte"
    )

    crud.create_recette(db, recette_data)

    recettes = db.query(models.Recette).all()
    assert len(recettes) == 1
    assert recettes[0].nom == "Takoyaki"
