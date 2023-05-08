"""
Database module for tv_recording
"""

import logging
import pathlib
import sqlite3
from typing import Union

from .config import Config


class Database:
    """
    Database for tv_recording
    """

    def __init__(self, logger: logging.Logger = None):
        """
        Construct a Database.
        """
        self.logger = logger or logging.getLogger(__name__)
        self.config = Config()
        self.db_path = self.config.get("database.path")
        self.db = sqlite3.connect(self.db_path.as_posix())
        self.db.row_factory = sqlite3.Row
        self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS recordings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT NOT NULL,
                start_time INTEGER NOT NULL,
                end_time INTEGER,
                UNIQUE (path)
            )
            """
        )
        self.db.commit()

    def add_recording(
        self,
        path: Union[str, pathlib.Path],
        start_time: int,
    ):
        """
        Add a recording to the database.
        """
        self.logger.info("tv_recording.db.Database.add_recording()")
        path = pathlib.Path(path).absolute().as_posix()
        self.db.execute(
            """
            INSERT INTO recordings (
                path,
                start_time
            )
            VALUES (?, ?)
            """,
            (path, start_time),
        )
        self.db.commit()

    def set_end_time(
        self,
        path: Union[str, pathlib.Path],
        end_time: int,
    ):
        """
        Set the end time for a recording.
        """
        self.logger.info("tv_recording.db.Database.set_end_time()")
        path = pathlib.Path(path).absolute().as_posix()
        self.db.execute(
            """
            UPDATE recordings
            SET end_time = ?
            WHERE path = ?
            """,
            (end_time, path),
        )
        self.db.commit()

    def get_active_recordings(self):
        """
        Get the active recording.
        """
        self.logger.debug("tv_recording.db.Database.get_active_recording()")
        return self.db.execute(
            """
            SELECT *
            FROM recordings
            WHERE end_time IS NULL
            """
        ).fetchall()
