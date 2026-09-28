import sqlite3
import os

DB_PATH = "gold_source.db"

def init_gold_db():
    # Deterministic: only create the Gold Source DB if it does not already exist
    if os.path.exists(DB_PATH):
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open("init/schema/gold_schema.sql") as f:
            cursor.executescript(f.read)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_gold_db()