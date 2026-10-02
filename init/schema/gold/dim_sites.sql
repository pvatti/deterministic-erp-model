CREATE TABLE IF NOT EXISTS dim_sites (
    site_id INTEGER PRIMARY KEY,
    site_code TEXT NOT NULL,
    site_name TEXT,
    region TEXT,
    status TEXT,
    is_active INTEGER,
    created_at TEXT,
    updated_at TEXT,
    source_system TEXT
);
