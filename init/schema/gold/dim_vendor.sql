CREATE TABLE IF NOT EXISTS dim_vendor (
    vendor_id INTEGER PRIMARY KEY,
    vendor_code TEXT NOT NULL,
    vendor_name TEXT,
    vendor_type TEXT,
    payment_terms TEXT,
    country TEXT,
    is_active INTEGER,
    created_at TEXT,
    updated_at TEXT,
    source_system TEXT
);
