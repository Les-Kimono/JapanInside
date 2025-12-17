from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi.responses import HTMLResponse, JSONResponse
from utils.carte_gen import generate_map_html, villes_data, itineraire, generate_japan_map

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

@app.get("/api/carte")
def get_carte():
    return HTMLResponse(content=generate_map_html())

# Route pour la carte interactive
@app.get("/carte", response_class=HTMLResponse)
async def get_carte():
    """Retourne la carte HTML interactive"""
    html_content = generate_map_html()
    return HTMLResponse(content=html_content)

# API pour les données des villes
@app.get("/api/villes")
async def get_all_villes():
    """Retourne toutes les villes disponibles"""
    return JSONResponse(content=villes_data)

@app.get("/api/villes/{nom_ville}")
async def get_ville(nom_ville: str):
    """Retourne les détails d'une ville spécifique"""
    ville_key = nom_ville.capitalize()
    if ville_key not in villes_data:
        raise HTTPException(status_code=404, detail=f"Ville {nom_ville} non trouvée")
    return villes_data[ville_key]

@app.get("/api/itineraire")
async def get_itineraire_complet():
    """Retourne l'itinéraire complet"""
    return {
        "itineraire": itineraire,
        "etapes": [
            {
                "ordre": i+1,
                "ville": ville,
                "coords": [villes_data[ville]["latitude"], villes_data[ville]["longitude"]]
            }
            for i, ville in enumerate(itineraire[:-1])  # Exclure le dernier Tokyo
        ]
    }

# Route pour générer une nouvelle carte
@app.post("/api/carte/generate")
async def generate_new_map():
    """Génère une nouvelle carte et la sauvegarde"""
    try:
        output_path = "static/carte_japon_latest.html"
        generate_japan_map(output_path)
        return {"message": "Carte générée avec succès", "path": output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

# Route pour obtenir une page détaillée d'une ville
@app.get("/ville/{nom_ville}", response_class=HTMLResponse)
async def get_ville_page(nom_ville: str):
    """Page détaillée pour une ville spécifique"""
    ville_key = nom_ville.capitalize()
    if ville_key not in villes_data:
        raise HTTPException(status_code=404, detail="Ville non trouvée")

    ville = villes_data[ville_key]

    # Générer le HTML pour la page de la ville
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{ville['nom']} - Japan Inside</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                overflow: hidden;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }}
            .header {{
                background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
                color: white;
                padding: 40px;
                text-align: center;
            }}
            .header h1 {{
                font-size: 3rem;
                margin: 0;
            }}
            .header p {{
                font-size: 1.2rem;
                opacity: 0.9;
                margin-top: 10px;
            }}
            .content {{
                padding: 40px;
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 40px;
            }}
            .info-section {{
                background: #f8f9fa;
                padding: 30px;
                border-radius: 15px;
            }}
            .attractions-section {{
                background: #f0f7ff;
                padding: 30px;
                border-radius: 15px;
            }}
            h2 {{
                color: #2c3e50;
                border-bottom: 3px solid #667eea;
                padding-bottom: 10px;
                margin-top: 0;
            }}
            .back-btn {{
                display: inline-block;
                padding: 12px 30px;
                background: #667eea;
                color: white;
                text-decoration: none;
                border-radius: 50px;
                font-weight: bold;
                margin-top: 20px;
                transition: all 0.3s;
            }}
            .back-btn:hover {{
                background: #5a6fd8;
                transform: translateY(-2px);
            }}
            .map-container {{
                height: 300px;
                border-radius: 15px;
                overflow: hidden;
                margin-top: 20px;
                border: 3px solid #667eea;
            }}
            @media (max-width: 768px) {{
                .content {{
                    grid-template-columns: 1fr;
                }}
                .header h1 {{
                    font-size: 2rem;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🇯🇵 {ville['nom']}</h1>
                <p>{ville['description']}</p>
            </div>
            
            <div class="content">
                <div class="info-section">
                    <h2>📊 Informations</h2>
                    <p><strong>Population:</strong> {ville['population']}</p>
                    <p><strong>Coordonnées:</strong> {ville['latitude']}°N, {ville['longitude']}°E</p>
                    
                    {f'''
                    <div style="margin-top: 20px;">
                        <h3>🌤️ Climat & Spécialités</h3>
                        <p><strong>Climat:</strong> {ville['informations_supp']['climat']}</p>
                        <p><strong>Meilleure saison:</strong> {ville['informations_supp']['meilleure_saison']}</p>
                        <p><strong>Spécialités culinaires:</strong> {ville['informations_supp']['specialites']}</p>
                    </div>
                    ''' if ville.get('informations_supp') else ''}
                    
                    <a href="/carte" class="back-btn">← Retour à la carte</a>
                </div>
                
                <div class="attractions-section">
                    <h2>🏛️ Attractions</h2>
                    <ul>
                        {''.join([f'<li style="margin: 10px 0; padding: 10px; background: white; border-radius: 8px;">{attr}</li>' for attr in ville['attractions']])}
                    </ul>
                    
                    <div class="map-container">
                        <iframe 
                            width="100%" 
                            height="100%" 
                            frameborder="0" 
                            scrolling="no" 
                            marginheight="0" 
                            marginwidth="0" 
                            src="https://www.openstreetmap.org/export/embed.html?bbox={ville['longitude']-0.1},{ville['latitude']-0.1},{ville['longitude']+0.1},{ville['latitude']+0.1}&layer=mapnik&marker={ville['latitude']},{ville['longitude']}">
                        </iframe>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(content=html_content)

# Routes existantes de votre API
@app.get('/api/hello')
def hello_world():
    return {"message": "Bienvenue sur Japan Inside API!"}

@app.get("/api/articles", response_model=list[schemas.Article])
def read_articles(db: Session = Depends(get_db)):
    """Retourne tous les articles"""
    return crud.get_articles(db)

@app.post("/api/articles", response_model=schemas.Article)
def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    """Crée un nouvel article"""
    return crud.create_article(db, article)

@app.get("/api/recettes", response_model=list[schemas.Recette])
def read_recettes(db: Session = Depends(get_db)):
    """Retourne toutes les recettes"""
    return crud.get_recettes(db)

@app.post("/api/recettes", response_model=schemas.Recette)
def create_recette(recette: schemas.RecetteCreate, db: Session = Depends(get_db)):
    """Crée une nouvelle recette"""
    return crud.create_recette(db, recette)

# Route de santé de l'API
@app.get("/health")
async def health_check():
    """Vérifie l'état de l'API"""
    return {
        "status": "healthy",
        "service": "Japan Inside API",
        "version": "1.0.0",
        "endpoints": {
            "carte": "/carte",
            "villes": "/api/villes",
            "itineraire": "/api/itineraire",
            "articles": "/api/articles",
            "recettes": "/api/recettes"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
