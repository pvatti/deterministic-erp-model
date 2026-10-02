CREATE TABLE IF NOT EXISTS fact_work_order (
    work_order_id INTEGER PRIMARY KEY,
    wo_number TEXT NOT NULL,
    site_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    planned_qty REAL,
    completed_qty REAL,
    scrap_qty REAL,
    start_date TEXT,
    end_date TEXT,
    duration_hours REAL,
    labor_cost REAL,
    material_cost REAL,
    total_cost REAL,
    created_at TEXT,
    updated_at TEXT,
    source_system TEXT
);
