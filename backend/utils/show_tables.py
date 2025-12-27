"""Inspect and display tables and their data in the database."""

from utils.database import SessionLocal, engine
from sqlalchemy import inspect, text


def show_tables_and_data():
    """Display all tables in the database and their contents.

    Connects to the database, lists all tables, and prints each table's
    columns and rows. Empty tables are indicated as '(vide)'.
    """
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    print("\n📦 Tables in the database:")
    for table in tables:
        print(f"- {table}")

    db = SessionLocal()

    for table in tables:
        print(f"\n📊 Contents of table '{table}':")

        result = db.execute(text(f"SELECT * FROM {table}"))
        rows = result.fetchall()

        if not rows:
            print("  (empty)")
            continue

        # Columns
        print("  Columns:", list(result.keys()))

        # Rows
        for row in rows:
            print(" ", tuple(row))

    db.close()


if __name__ == "__main__":
    show_tables_and_data()
