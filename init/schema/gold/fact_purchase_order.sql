CREATE TABLE IF NOT EXISTS fact_purchase_order (
    po_line_id INTEGER PRIMARY KEY,
    po_number TEXT NOT NULL,
    po_line_number INTEGER NOT NULL,
    vendor_id INTEGER NOT NULL,
    site_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    ordered_qty REAL,
    received_qty REAL,
    unit_price REAL,
    extended_price REAL,
    order_date TEXT,
    promised_date TEXT,
    received_date TEXT,
    lead_time_days REAL,
    created_at TEXT,
    updated_at TEXT,
    source_system TEXT
);
