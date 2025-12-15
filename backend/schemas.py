from pydantic import BaseModel

class ArticleBase(BaseModel):
    titre: str
contenu: str

class ArticleCreate(ArticleBase):
    pass

class Article(ArticleBase):
    id: int
class Config:
    orm_mode = True

class RecetteBase(BaseModel):
    nom: str
description: str
ingredients: str

class RecetteCreate(RecetteBase):
    pass

class Recette(RecetteBase):
    id: int
class Config:
    orm_mode = True