import sqlite3
from pathlib import Path


class DatabaseConnection:
    """Singleton wrapper around the SQLite connection."""

    _instance = None

    def __new__(cls, db_path: str | Path = "library.db"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, db_path: str | Path = "library.db"):
        if self._initialized:
            return
        self.db_path = str(db_path)
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute(
            """CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT NOT NULL UNIQUE,
                available INTEGER NOT NULL DEFAULT 1
            )"""
        )
        self.connection.commit()
        self._initialized = True

    def execute(self, query: str, parameters: tuple = ()):
        cursor = self.connection.execute(query, parameters)
        self.connection.commit()
        return cursor

    def close(self) -> None:
        self.connection.close()
        type(self)._instance = None
