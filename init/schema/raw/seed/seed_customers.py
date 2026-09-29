import sqlite3

DB_PATH = "external_erp.db"

def seed_customers():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM customers;")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    customers = [
        (1, "CUST-001", "Acme Retail", "active"),
        (2, "CUST-002", "NorthStar Distribution", "active"),
        (3, "CUST-003", "Prime Industrial Supply", "active")
    ]

    cursor.executemany("""
        INSERT INTO customers (customer_id, customer_code, customer_name, status)
        VALUES (?, ?, ?, ?);
    """, customers)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    seed_customers()
