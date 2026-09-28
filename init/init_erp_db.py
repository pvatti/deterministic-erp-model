import sqlite3
import os

DB_PATH = "external_erp.db"

def init_erp_db():

    #Deterministic: only create the ERP DB if it does not already exist
    if os.path.exists(DB_PATH):
        return

    conn = sqlite3.connect("external_erp.db")
    cursor = conn.cursor()

    with open("init/schema/erp_schema.sql") as f:
        cursor.executescript(f.read)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_erp_db()