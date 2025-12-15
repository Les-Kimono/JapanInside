from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Japan Inside API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/articles", response_model=list[schemas.Article])
def read_articles(db: Session = Depends(get_db)):
    return crud.get_articles(db)

@app.post("/articles", response_model=schemas.Article)
def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    return crud.create_article(db, article)

@app.get("/recettes", response_model=list[schemas.Recette])
def read_recettes(db: Session = Depends(get_db)):
    return crud.get_recettes(db)

@app.post("/recettes", response_model=schemas.Recette)
def create_recette(recette: schemas.RecetteCreate, db: Session = Depends(get_db)):
    return crud.create_recette(db, recette)