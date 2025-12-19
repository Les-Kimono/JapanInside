from sqlalchemy import inspect, text
from database import engine, SessionLocal


def show_tables_and_data():
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    print("\n📦 Tables dans la base :")
    for table in tables:
        print(f"- {table}")

    db = SessionLocal()

    for table in tables:
        print(f"\n📊 Contenu de la table '{table}':")

        result = db.execute(text(f"SELECT * FROM {table}"))
        rows = result.fetchall()

        if not rows:
            print("  (vide)")
            continue

        # Colonnes
        print("  Colonnes :", list(result.keys()))

        # Lignes
        for row in rows:
            print(" ", tuple(row))

    db.close()


if __name__ == "__main__":
    show_tables_and_data()
