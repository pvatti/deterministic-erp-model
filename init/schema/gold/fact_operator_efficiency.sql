CREATE TABLE IF NOT EXISTS fact_operator_efficiency (
    efficiency_id INTEGER PRIMARY KEY,
    operator_id INTEGER NOT NULL,
    machine_id INTEGER,
    site_id INTEGER NOT NULL,
    work_order_id INTEGER,
    start_time TEXT,
    end_time TEXT,
    runtime_minutes REAL,
    downtime_minutes REAL,
    total_minutes REAL,
    utilization REAL,
    shift TEXT,
    created_at TEXT,
    updated_at TEXT,
    source_system TEXT
);
