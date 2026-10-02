CREATE TABLE IF NOT EXISTS fact_shipment (
    shipment_line_id INTEGER PRIMARY KEY,
    shipment_number TEXT NOT NULL,
    shipment_line_number INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    site_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    shipped_qty REAL,
    invoiced_qty REAL,
    revenue REAL,
    discount REAL,
    shipment_date TEXT,
    promised_date TEXT,
    delivered_date TEXT,
    delivery_days REAL,
    created_at TEXT,
    updated_at TEXT,
    source_system TEXT
);
