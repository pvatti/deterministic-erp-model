import sqlite3

DB_PATH = "external_erp.db"

def seed_routing():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM routing_raw;")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    routing = [
        # FG100 routing at Raleigh (site 1)
        (1, 1, 1, 1, "CUT", 1, 15.0, "system", None),
        (2, 1, 1, 2, "PRESS", 2, 10.0, "system", None),

        # FG100 routing at Cincinnati (site 2)
        (3, 1, 2, 1, "ASSEMBLE", 3, 20.0, "system", None)
    ]

    cursor.executemany("""
        INSERT INTO routing_raw (
            routing_id, item_id, site_id, step_number,
            operation_code, machine_id, standard_duration_minutes,
            updated_by, notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, routing)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    seed_routing()
