CREATE TABLE IF NOT EXISTS dim_machines (
    machine_id INTEGER PRIMARY KEY,
    machine_code TEXT NOT NULL,
    machine_name TEXT,
    machine_type TEXT,
    site_id INTEGER,
    manufacturer TEXT,
    model TEXT,
    status TEXT,
    is_active INTEGER,
    created_at TEXT,
    updated_at TEXT,
    source_system TEXT
);
