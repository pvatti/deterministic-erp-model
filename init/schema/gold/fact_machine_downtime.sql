CREATE TABLE IF NOT EXISTS fact_machine_downtime (
    downtime_id INTEGER PRIMARY KEY,
    machine_id INTEGER NOT NULL,
    operator_id INTEGER,
    site_id INTEGER NOT NULL,
    work_order_id INTEGER,
    start_time TEXT,
    end_time TEXT,
    downtime_minutes REAL,
    reason_code TEXT,
    reason_category TEXT,
    created_at TEXT,
    updated_at TEXT,
    source_system TEXT
);
