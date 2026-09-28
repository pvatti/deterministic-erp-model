import sqlite3

DB_PATH = "external_erp.db"

def seed_machines():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM machines;")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    machines = [
        (1, 1, "MC-RA-01", "Raleigh Cutter", "active"),
        (2, 1, "MC-RA-02", "Raleigh Press", "active"),
        (3, 2, "MC-CI-01", "Cincinnati Assembler", "active")
    ]

    cursor.executemany("""
        INSERT INTO machines (machine_id, site_id, machine_code, machine_name, status)
        VALUES (?, ?, ?, ?, ?);
    """, machines)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    seed_machines()
