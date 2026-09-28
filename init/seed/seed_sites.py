import sqlite3

DB_PATH = "externa_erp.db"

def seed_sites():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # only seed if table is empty
    cursor.execute("SELECT COUNT(*) FROM sites;")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    sites = [
        (1, "NC01", "Raleigh Plant", "Southeast", "active"),
        (2, "OH01", "Cincinnati Plant", "Midwest", "active"),
        (3, "TX01", "Dallas DC", "Southwest", "active")
    ]

    cursor.executemany("""
        INSERT INTO sites (site_id, site_code, site_name, region, status)
        VALUES (?, ?, ?, ?, ?);
    """, sites)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    seed_sites()