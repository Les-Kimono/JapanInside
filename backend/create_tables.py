from database import engine, Base
from models import Ville, Attraction, Recette 

from sqlalchemy import text


with engine.connect() as conn:
    conn.execution_options(isolation_level="AUTOCOMMIT")
    
    tables = conn.execute(
        text("SELECT tablename FROM pg_tables WHERE schemaname='public'")
    ).fetchall()
    
    for (table_name,) in tables:
        conn.execute(text(f'DROP TABLE IF EXISTS "{table_name}" CASCADE'))
    
print("Toutes les tables du schéma public ont été supprimées ✅")

Base.metadata.create_all(bind=engine)

print("Tables créées avec succès")