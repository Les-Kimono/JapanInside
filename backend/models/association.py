from sqlalchemy import Table, Column, Integer, ForeignKey
from utils.database import Base

ville_recette = Table(
    "ville_recette",
    Base.metadata,
    Column("ville_id", Integer, ForeignKey("villes.id"), primary_key=True),
    Column("recette_id", Integer, ForeignKey("recettes.id"), primary_key=True),
)
