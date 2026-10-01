import sqlite3
import os

RAW_DB = "data/raw.db"
RAW_SCHEMA = "init/raw/erp_schema.sql"
RAW_SEED_DIR = "init/raw/seed"


def create_raw_db():
    if not os.path.exists(RAW_DB):
        print("Creating RAW database...")
        conn = sqlite3.connect(RAW_DB)
        cursor = conn.cursor()

        with open(RAW_SCHEMA, "r", encoding="utf-8") as f:
            schema_sql = f.read()
            cursor.executescript(schema_sql)

        conn.commit()
        conn.close()
    else:
        print("RAW database already exists.")


def load_sql_seed_files():
    conn = sqlite3.connect(RAW_DB)
    cursor = conn.cursor()

    for filename in os.listdir(RAW_SEED_DIR):
        if filename.endswith(".sql"):
            sql_path = os.path.join(RAW_SEED_DIR, filename)
            print(f"Loading seed file: {filename}")

            with open(sql_path, "r", encoding="utf-8") as f:
                seed_sql = f.read()
                cursor.executescript(seed_sql)

    conn.commit()
    conn.close()


def run_raw_loader():
    create_raw_db()
    load_sql_seed_files()
    print("RAW layer successfully initialized.")


if __name__ == "__main__":
    run_raw_loader()
