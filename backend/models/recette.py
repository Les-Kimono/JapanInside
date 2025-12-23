from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from utils.database import Base
from .association import ville_recette

class Recette(Base):
    __tablename__ = "recettes"

    id = Column(Integer, primary_key=True)
    nom = Column(String(255), nullable=False)
    description = Column(Text)
    ingredients = Column(Text)
    
    villes = relationship("Ville", secondary=ville_recette, back_populates="recettes")
