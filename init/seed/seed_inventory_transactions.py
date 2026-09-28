import sqlite3

DB_PATH = "external_erp.db"

def seed_inventory_transactions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM inventory_transactions_raw;")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    txns = [
        (1, 1, 1, "RECEIPT", 150.0, "2026-01-01T08:00:00", 1, None),
        (2, 1, 2, "RECEIPT", 500.0, "2026-01-01T09:00:00", 2, None),
        (3, 2, 3, "ISSUE", -25.0, "2026-01-01T10:00:00", 3, "WIP consumption")
    ]

    cursor.executemany("""
        INSERT INTO inventory_transactions_raw (
            txn_id, site_id, item_id, txn_type, quantity,
            timestamp, reference_id, notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, txns)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    seed_inventory_transactions()
