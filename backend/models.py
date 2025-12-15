from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date
from database import Base

class Article(Base):
    __tablename__ = "articles"
id = Column(Integer, primary_key=True)
titre = Column(String(255))
contenu = Column(Text)

class Recette(Base):
    __tablename__ = "recettes"
id = Column(Integer, primary_key=True)
nom = Column(String(255))
description = Column(Text)
ingredients = Column(Text)