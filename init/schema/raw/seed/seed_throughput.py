import sqlite3

DB_PATH = "external_erp.db"

def seed_throughput():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM throughput_raw;")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    throughput = [
        (1, 1, 1, 1, 1, 1, 90.0, 5.0, "2026-01-02T14:00:00", "1st", None),
        (2, 2, 2, 3, 3, 3, 180.0, 10.0, "2026-01-03T15:00:00", "2nd", None)
    ]

    cursor.executemany("""
        INSERT INTO throughput_raw (
            throughput_id, site_id, work_order_id, machine_id,
            operator_id, units_produced, scrap_units,
            timestamp, shift_code, notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, throughput)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    seed_throughput()
