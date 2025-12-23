"""Main FastAPI application for Japan Inside API.

Provides endpoints for villes, attractions, recettes, and database management.
"""

import json

from utils.database import engine, Base
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import health
from routes import recettes
from routes import attractions
from routes import setup
from routes import villes

import models

with open("data/villes.json", "r", encoding="utf-8") as f:
    villes_data = json.load(f)


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Japan Inside API")
origins = ["http://localhost:5173", "http://127.0.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(recettes.router, prefix="/api", tags=["Recettes"])
app.include_router(attractions.router, prefix="/api", tags=["Attractions"])
app.include_router(setup.router, prefix="/api", tags=["Setup"])
app.include_router(villes.router, prefix="/api", tags=["Villes"])



@app.get("/")
def hello_world():
    """Return a simple status response."""
    return {}, 200

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
