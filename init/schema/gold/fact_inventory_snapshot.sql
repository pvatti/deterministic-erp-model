CREATE TABLE IF NOT EXISTS fact_inventory_snapshot (
    snapshot_id INTEGER PRIMARY KEY,
    snapshot_date TEXT NOT NULL,
    site_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    quantity_on_hand REAL,
    quantity_reserved REAL,
    quantity_available REAL,
    inventory_value REAL,
    created_at TEXT,
    updated_at TEXT,
    source_system TEXT
);
