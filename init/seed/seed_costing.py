import sqlite3

DB_PATH = "external_erp.db"

def seed_costing():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM costing_raw;")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    costing = [
        (1, 1, 1, 12.50, "2026-01-01", "system"),
        (2, 2, 1, 4.75, "2026-01-01", "system"),
        (3, 3, 2, 8.20, "2026-01-01", "system")
    ]

    cursor.executemany("""
        INSERT INTO costing_raw (cost_id, item_id, site_id, standard_cost, last_updated_at, updated_by)
        VALUES (?, ?, ?, ?, ?, ?);
    """, costing)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    seed_costing()
