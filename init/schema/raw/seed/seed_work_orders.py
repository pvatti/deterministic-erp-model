import sqlite3

DB_PATH = "external_erp.db"

def seed_work_orders():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM work_orders_raw;")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    work_orders = [
        (1, 1, 1, 100.0, "2026-01-02", "2026-01-03", "planned", "system"),
        (2, 2, 1, 200.0, "2026-01-02", "2026-01-04", "planned", "system")
    ]

    cursor.executemany("""
        INSERT INTO work_orders_raw (
            work_order_id, site_id, item_id, planned_quantity,
            scheduled_start, scheduled_end, status, created_by
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, work_orders)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    seed_work_orders()
