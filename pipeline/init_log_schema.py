import os
import sqlite3

# Detect project root (directory above /pipeline)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Default logging DB path
DEFAULT_LOG_DB = os.path.join(PROJECT_ROOT, "semantic_log.db")

# Logging schema directory
LOG_SCHEMA_DIR = os.path.join(PROJECT_ROOT, "init", "schema", "logging")


def init_log_schema(log_db_path: str = DEFAULT_LOG_DB):
    """
    Initializes the semantic logging schema.
    Loads all SQL files under init/schema/logging/ and executes them.
    Safe to run multiple times because SQL uses CREATE TABLE IF NOT EXISTS.
    """

    # Ensure the logging DB file exists (SQLite creates it automatically)
    conn = sqlite3.connect(log_db_path)
    cur = conn.cursor()

    # Ensure schema directory exists
    if not os.path.isdir(LOG_SCHEMA_DIR):
        raise FileNotFoundError(f"Logging schema directory not found: {LOG_SCHEMA_DIR}")

    # Execute all .sql files in the logging schema directory
    for file in os.listdir(LOG_SCHEMA_DIR):
        if file.endswith(".sql"):
            schema_path = os.path.join(LOG_SCHEMA_DIR, file)
            with open(schema_path, "r") as f:
                sql_script = f.read()
                cur.executescript(sql_script)

    conn.commit()
    conn.close()

    print(f"Semantic logging schema initialized at: {log_db_path}")
