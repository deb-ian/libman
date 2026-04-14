import sqlite3
from pathlib import Path


def initialize_database():
    """Initialize the library management system database from the existing schema."""
    project_root = Path(__file__).parent
    db_path = project_root / "library.db"
    schema_path = project_root / "schema.sql"

    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    conn = sqlite3.connect(db_path)
    with schema_path.open("r", encoding="utf-8") as schema_file:
        schema_sql = schema_file.read()

    conn.executescript(schema_sql)
    conn.close()
    print(f"Database initialized at {db_path}")


if __name__ == "__main__":
    initialize_database()
