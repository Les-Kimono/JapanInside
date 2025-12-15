"""from sqlalchemy.orm import Session
import models, schemas

def create_article(db: Session, article: schemas.ArticleCreate):
    db_article = models.Article(**article.dict())
db.add(db_article)
db.commit()
db.refresh(db_article)
return db_article

def get_articles(db: Session):
    return db.query(models.Article).all()

def create_recette(db: Session, recette: schemas.RecetteCreate):
    db_recette = models.Recette(**recette.dict())
db.add(db_recette)
db.commit()
db.refresh(db_recette)
return db_recette

def get_recettes(db: Session):
    return db.query(models.Recette).all()"""