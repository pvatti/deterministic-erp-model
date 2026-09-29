import sqlite3

DB_PATH = "external_erp.db"

def seed_operators():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM operators;")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    operators = [
        (1, 1, "OP-RA-01", "Alice Johnson", "Assembler"),
        (2, 1, "OP-RA-02", "Mark Lee", "Machine Operator"),
        (3, 2, "OP-CI-01", "Priya Patel", "Technician")
    ]

    cursor.executemany("""
        INSERT INTO operators (operator_id, site_id, operator_code, operator_name, role)
        VALUES (?, ?, ?, ?, ?);
    """, operators)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    seed_operators()
