import sqlite3

DB_PATH = "external_erp.db"

def seed_items():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM items;")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    items = [
        (1, "FG100", "Finished Good A", "FG", "EA", "active"),
        (2, "RM200", "Raw Material B", "RM", "KG", "active"),
        (3, "WIP300", "Work In Process C", "WIP", "EA", "active")
    ]

    cursor.executemany("""
        INSERT INTO items (item_id, item_sku, item_name, item_type, uom, status)
        VALUES (?, ?, ?, ?, ?, ?);
    """, items)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    seed_items()
