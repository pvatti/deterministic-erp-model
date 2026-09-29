import sqlite3

DB_PATH = "external_erp.db"

def seed_inventory():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM inventory_raw;")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    inventory = [
        (1, 1, 1, 150.0, "A1", "2026-01-01", "system", None),
        (2, 1, 2, 500.0, "RM-01", "2026-01-01", "system", None),
        (3, 2, 3, 75.0, "WIP-02", "2026-01-01", "system", None)
    ]

    cursor.executemany("""
        INSERT INTO inventory_raw (
            inventory_id, site_id, item_id, quantity_on_hand,
            location_code, last_updated_at, last_updated_by, notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, inventory)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    seed_inventory()
