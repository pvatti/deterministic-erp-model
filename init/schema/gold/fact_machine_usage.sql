CREATE TABLE IF NOT EXISTS fact_machine_usage (
    usage_id INTEGER PRIMARY KEY,
    machine_id INTEGER NOT NULL,
    operator_id INTEGER,
    site_id INTEGER NOT NULL,
    work_order_id INTEGER,
    start_time TEXT,
    end_time TEXT,
    runtime_minutes REAL,
    downtime_minutes REAL,
    total_minutes REAL,
    reason_code TEXT,
    created_at TEXT,
    updated_at TEXT,
    source_system TEXT
);
