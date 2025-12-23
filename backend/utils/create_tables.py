"""
File that contains a method to create all the tables for PostgreSQL.

Authors:
    Justine HAKIM
    Aman GHAZANFAR
"""

from .database import Base, engine
from sqlalchemy import text


def execute():
    """Create all tables in the public PostgreSQL schema."""
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


if __name__ == "__main__":
    execute()
