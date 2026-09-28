import sqlite3

DB_PATH = "external_erp.db"

def seed_vendors():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM vendors;")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    vendors = [
        (1, "VEND-001", "Global Metals Inc", "active"),
        (2, "VEND-002", "Precision Plastics", "active"),
        (3, "VEND-003", "Industrial Chemicals LLC", "active")
    ]

    cursor.executemany("""
        INSERT INTO vendors (vendor_id, vendor_code, vendor_name, status)
        VALUES (?, ?, ?, ?);
    """, vendors)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    seed_vendors()
