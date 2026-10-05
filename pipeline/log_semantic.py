import os
import sqlite3
from datetime import datetime

# Detect project root (directory above /pipeline)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Default logging DB path
DEFAULT_LOG_DB = os.path.join(PROJECT_ROOT, "semantic_log.db")


def get_connection(log_db_path: str = DEFAULT_LOG_DB):
    """Return a SQLite connection to the semantic log database."""
    return sqlite3.connect(log_db_path)


def log_semantic_event(
    model_name: str,
    start_time: float,
    end_time: float,
    status: str,
    rows_returned: int | None = None,
    validation_passed: bool | None = None,
    validation_failures: int | None = None,
    error_message: str | None = None,
    log_db_path: str = DEFAULT_LOG_DB,
):
    """
    Insert a semantic execution event into the semantic_log table.
    Assumes the table already exists (created by init_log_schema).
    """

    conn = get_connection(log_db_path)
    cur = conn.cursor()

    start_iso = datetime.fromtimestamp(start_time).isoformat()
    end_iso = datetime.fromtimestamp(end_time).isoformat()
    duration_ms = int((end_time - start_time) * 1000)

    cur.execute(
        """
        INSERT INTO semantic_log (
            model_name,
            start_time,
            end_time,
            duration_ms,
            status,
            rows_returned,
            validation_passed,
            validation_failures,
            error_message
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """,
        (
            model_name,
            start_iso,
            end_iso,
            duration_ms,
            status,
            rows_returned,
            int(validation_passed) if validation_passed is not None else None,
            validation_failures,
            error_message,
        ),
    )

    conn.commit()
    conn.close()
