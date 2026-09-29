import sqlite3

DB_PATH = "external_erp.db"

def seed_bom():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM bom_raw;")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    bom = [
        # FG100 requires RM200 (2 units) and WIP300 (1 unit)
        (1, 1, 2, 2.0, 1, "A", "2026-01-01", None, "system", None),
        (2, 1, 3, 1.0, 1, "A", "2026-01-01", None, "system", None)
    ]

    cursor.executemany("""
        INSERT INTO bom_raw (
            bom_id, item_id, component_item_id, quantity_per,
            site_id, version, effective_from, effective_to,
            updated_by, notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, bom)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    seed_bom()
