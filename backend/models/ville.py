from sqlalchemy import Column, Integer, String, Text, Float
from sqlalchemy.orm import relationship
from utils.database import Base
from .association import ville_recette
class Ville(Base):
    __tablename__ = "villes"

    id = Column(Integer, primary_key=True)
    nom = Column(String(255), nullable=False)
    position = Column(Integer)
    description = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    population = Column(Integer)
    meilleure_saison = Column(String(100))
    climat = Column(Text)

    attractions = relationship(
        "Attraction", back_populates="ville", cascade="all, delete"
    )
    recettes = relationship(
        "Recette", secondary=ville_recette, back_populates="villes"
    )
