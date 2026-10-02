CREATE TABLE IF NOT EXISTS fact_sales (
    sales_line_id INTEGER PRIMARY KEY,
    invoice_number TEXT NOT NULL,
    invoice_line_number INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    site_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    sold_qty REAL,
    unit_price REAL,
    extended_price REAL,
    discount REAL,
    net_revenue REAL,
    invoice_date TEXT,
    created_at TEXT,
    updated_at TEXT,
    source_system TEXT
);
