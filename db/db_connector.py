import sqlite3
from contextlib import contextmanager
from frozen_v1.fs_root import SQLITE_DB

@contextmanager
def get_sqlite_conn():
    conn=sqlite3.connect(SQLITE_DB)
    conn.execute("PRAGMA journal_mode=WAL;")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_sqlite_db():
    with get_sqlite_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS measurements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            parameter TEXT,
            value REAL,
            unit TEXT,
            timestamp_utc TEXT,
            city TEXT,
            source TEXT,
            ingestion_time TEXT)
        """)