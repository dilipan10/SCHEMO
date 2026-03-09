import mysql.connector
from mysql.connector import Error
import os

# ── Database connection configuration ────────────────────────
DB_CONFIG = {
    "host":     os.environ.get("DB_HOST") or "localhost",
    "user":     os.environ.get("DB_USER") or "root",
    "password": os.environ.get("DB_PASS") or "Haripriya@38",
    "database": os.environ.get("DB_NAME") or "schemo_db",
    "charset":  "utf8mb4",
    "collation": "utf8mb4_unicode_ci",
}


def get_connection():
    """Return a fresh MySQL connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as exc:
        raise ConnectionError(f"[DB] Could not connect to MySQL: {exc}") from exc


def execute_query(query: str, params: tuple = (), fetch: bool = False):
    """
    Execute a DML query (INSERT / UPDATE / DELETE) or a SELECT.

    Parameters
    ----------
    query  : SQL string with %s placeholders
    params : tuple of values for placeholders
    fetch  : if True, return all rows as list-of-dicts
    Returns
    -------
    list[dict] when fetch=True, else lastrowid (int)
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params)
        if fetch:
            result = cursor.fetchall()
            return result
        conn.commit()
        return cursor.lastrowid
    except Error as exc:
        conn.rollback()
        raise RuntimeError(f"[DB] Query failed: {exc}\nSQL: {query}") from exc
    finally:
        cursor.close()
        conn.close()
