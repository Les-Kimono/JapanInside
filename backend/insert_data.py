import json
from sqlalchemy.orm import Session
from database import SessionLocal
import models

JSON_FILE = "villes.json"

def execute():
    db: Session = SessionLocal()

    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            villes_data = json.load(f)

        for ville_data in villes_data:
            # Créer la ville
            ville = models.Ville(
                nom=ville_data["nom"],
                position=ville_data.get("position"),
                description=ville_data.get("description"),
                latitude=ville_data.get("latitude"),
                longitude=ville_data.get("longitude"),
                population=ville_data.get("population"),
                meilleure_saison=ville_data.get("meilleure_saison"),
                climat=ville_data.get("climat")
            )
            db.add(ville)
            db.flush()  # flush pour obtenir l'id de la ville

            # Ajouter les attractions
            for attr_data in ville_data.get("attractions", []):
                attraction = models.Attraction(
                    nom=attr_data["nom"],
                    description=attr_data.get("description"),
                    ville_id=ville.id
                )
                db.add(attraction)

            # Ajouter les recettes
            for rec_data in ville_data.get("recettes", []):
                recette = models.Recette(
                    nom=rec_data["nom"],
                    description=rec_data.get("description"),
                    ingredients=rec_data.get("ingredients")
                )
                db.add(recette)
                db.flush()
                # Lier la recette à la ville
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
