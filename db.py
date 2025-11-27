import sqlite3
from contextlib import closing

DATABASE = "solicitudes.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row 
    return conn


def init_db():
    with closing(get_connection()) as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS solicitudes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                folio TEXT NOT NULL,
                fecha TEXT NOT NULL,
                solicitante TEXT NOT NULL,
                tipo TEXT NOT NULL,
                estado TEXT NOT NULL,
                descripcion TEXT
            );
            """
        )
        conn.commit()
