from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
import os
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Japan Inside API")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/api/hello')
def hello_world():
    return {"message": "Hello World"}
@app.get('/')
def hello_world():
    DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///:memory:"  
)
    print(DATABASE_URL)
    return {}, 200
@app.get("/api/articles", response_model=list[schemas.Article])
def read_articles(db: Session = Depends(get_db)):
    return crud.get_articles(db)

@app.post("/api/articles", response_model=schemas.Article)
def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    return crud.create_article(db, article)

@app.get("/api/recettes", response_model=list[schemas.Recette])
def read_recettes(db: Session = Depends(get_db)):
    return crud.get_recettes(db)

@app.post("/api/recettes", response_model=schemas.Recette)
def create_recette(recette: schemas.RecetteCreate, db: Session = Depends(get_db)):
    return crud.create_recette(db, recette)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
