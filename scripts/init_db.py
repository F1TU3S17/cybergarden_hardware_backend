"""Utility to initialize the database (create tables).

Run with:
    .\.venv\Scripts\Activate.ps1
    python scripts\init_db.py
"""
from app.db.session import init_db


if __name__ == "__main__":
    init_db()
    print("Database initialized (tables created)")
