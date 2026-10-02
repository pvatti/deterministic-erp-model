CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id INTEGER PRIMARY KEY,
    customer_code TEXT NOT NULL,
    customer_name TEXT,
    customer_type TEXT,
    region TEXT,
    country TEXT,
    is_active INTEGER,
    created_at TEXT,
    updated_at TEXT,
    source_system TEXT
);
