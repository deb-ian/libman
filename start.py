import sqlite3
from pathlib import Path


def initialize_database():
    """Initialize the library management system database from the existing schema."""
    project_root = Path(__file__).parent
    db_path = project_root / "library.db"
    schema_path = project_root / "schema.sql"

    conn = sqlite3.connect(db_path)
    with schema_path.open("r", encoding="utf-8") as schema_file:
        schema_sql = schema_file.read()

    conn.executescript(schema_sql)
    conn.close()
    print(f"Database initialized at {db_path}")


if __name__ == "__main__":
    if not (Path(__file__).parent / "library.db").exists():
        initialize_database()
    else:
        print("Database already exists. Initialization skipped.")
