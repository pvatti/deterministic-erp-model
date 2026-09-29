import sqlite3

DB_PATH = "external_erp.db"

def seed_scrap():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM scrap_raw;")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    scrap = [
        (1, 1, 1, 5.0, "Material defect", "2026-01-02T14:30:00", 1),
        (2, 2, 3, 10.0, "Assembly error", "2026-01-03T16:00:00", 3)
    ]

    cursor.executemany("""
        INSERT INTO scrap_raw (
            scrap_id, site_id, item_id, quantity,
            reason, timestamp, operator_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, scrap)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    seed_scrap()
