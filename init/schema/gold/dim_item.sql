CREATE TABLE IF NOT EXISTS dim_item (
    item_id INTEGER PRIMARY KEY,
    item_sku TEXT NOT NULL,
    item_name TEXT,
    item_description TEXT,
    category TEXT,
    subcategory TEXT,
    unit_of_measure TEXT,
    standard_cost REAL,
    cost_method TEXT,
    is_active INTEGER,
    created_at TEXT,
    updated_at TEXT,
    source_system TEXT
);
