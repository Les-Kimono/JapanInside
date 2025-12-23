"""Insert initial data into the database from a JSON file."""

import json

import models
from .database import SessionLocal
from sqlalchemy.orm import Session

JSON_FILE = "data/villes.json"


def execute() -> None:
    """
    Insert.

    Villes, attractions, and recettes from the JSON file into the database.
    """
    db: Session = SessionLocal()

    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            villes_data = json.load(f)

        for ville_data in villes_data:
            # Create Ville
            ville = models.Ville(
                nom=ville_data["nom"],
                position=ville_data.get("position"),
                description=ville_data.get("description"),
                latitude=ville_data.get("latitude"),
                longitude=ville_data.get("longitude"),
                population=ville_data.get("population"),
                meilleure_saison=ville_data.get("meilleure_saison"),
                climat=ville_data.get("climat"),
            )
            db.add(ville)
            db.flush()  # flush to get the ville.id

            # Add Attractions
            for attr_data in ville_data.get("attractions", []):
                attraction = models.Attraction(
                    nom=attr_data["nom"],
                    description=attr_data.get("description"),
                    longitude=attr_data.get("longitude"),
                    latitude=attr_data.get("latitude"),
                    ville_id=ville.id,
                )
                db.add(attraction)

            # Add Recettes
            for rec_data in ville_data.get("recettes", []):
                recette = models.Recette(
                    nom=rec_data["nom"],
                    description=rec_data.get("description"),
                    ingredients=rec_data.get("ingredients"),
                )
                db.add(recette)
                db.flush()
                # Link recette to ville
                ville.recettes.append(recette)

        db.commit()
        print("✅ Toutes les données ont été insérées avec succès !")

    except Exception as e:
        db.rollback()
        print("❌ Une erreur est survenue :", e)
    finally:
        db.close()


if __name__ == "__main__":
    execute()
