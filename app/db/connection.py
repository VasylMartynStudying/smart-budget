import sqlite3
import sys
from pathlib import Path

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('INCOME', 'EXPENSE'))
);
"""


def application_root() -> Path:
    """
    Writable app directory in source tree and after PyInstaller freeze.

    PyInstaller's ``sys._MEIPASS`` is a temporary extract dir (especially in
    onefile mode), so a persistent SQLite file must live next to the exe.
    """

    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[2]


def default_db_path() -> Path:
    return application_root() / "data" / "smart_budget.db"


def connect(db_path: str | Path = ":memory:") -> sqlite3.Connection:
    if db_path != ":memory:":
        path = Path(db_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        db_path = path

    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_schema(connection: sqlite3.Connection) -> None:
    connection.executescript(SCHEMA_SQL)
    connection.commit()
