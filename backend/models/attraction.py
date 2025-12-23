from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from utils.database import Base

class Attraction(Base):
    __tablename__ = "attractions"

    id = Column(Integer, primary_key=True)
    nom = Column(String(255), nullable=False)
    description = Column(Text)
    longitude = Column(Float)
    latitude = Column(Float)
    ville_id = Column(Integer, ForeignKey("villes.id"), nullable=False)


    ville = relationship("Ville", back_populates="attractions")
