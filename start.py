# type: ignore
"""
TODO: Make this into a cli tool with an full update manager
"""

import importlib.util
import sqlite3
import subprocess
import sys
from pathlib import Path

def check_dependencies():
    try:
        import flask
        import flask_admin
        import sqlalchemy
    except ImportError:
        print("Key dependencies not found. Installing...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", f"{Path(__file__).parent.resolve()}/requirements.txt"]
        )


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
    check_dependencies()
    from adpan.main import main
    if not (Path(__file__).parent / "library.db").exists():
        initialize_database()
        main()
    else:
        print("Database already exists. Initialization skipped.")
        main()
    
