from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, Table, JSON
from sqlalchemy.orm import relationship
from database import Base

ville_recette = Table(
    "ville_recette",
    Base.metadata,
    Column("ville_id", Integer, ForeignKey("villes.id"), primary_key=True),
    Column("recette_id", Integer, ForeignKey("recettes.id"), primary_key=True),
)

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
   
    
    attractions = relationship("Attraction", back_populates="ville", cascade="all, delete")
    recettes = relationship("Recette", secondary=ville_recette, back_populates="villes")


class Attraction(Base):
    __tablename__ = "attractions"

    id = Column(Integer, primary_key=True)
    nom = Column(String(255), nullable=False)
    description = Column(Text)

    ville_id = Column(Integer, ForeignKey("villes.id"), nullable=False)
    ville = relationship("Ville", back_populates="attractions")


class Recette(Base):
    __tablename__ = "recettes"

    id = Column(Integer, primary_key=True)
    nom = Column(String(255), nullable=False)
    description = Column(Text)
    ingredients = Column(Text)

    villes = relationship("Ville", secondary=ville_recette, back_populates="recettes")
