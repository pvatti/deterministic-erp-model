CREATE TABLE IF NOT EXISTS dim_operators (
    operator_id INTEGER PRIMARY KEY,
    operator_code TEXT NOT NULL,
    operator_name TEXT,
    operator_role TEXT,
    site_id INTEGER,
    shift TEXT,
    status TEXT,
    is_active INTEGER,
    created_at TEXT,
    updated_at TEXT,
    source_system TEXT
);
