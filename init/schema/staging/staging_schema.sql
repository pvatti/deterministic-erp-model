---------------------------------------------------------------------------
-- STAGING SCHEMA
-- This layer receives validated, normalized, canonicalized data from RAW.
-- All business rules, transformations, and exception logging occur here.
---------------------------------------------------------------------------


---------------------------------------------------------------------------
-- EXCEPTIONS & AUDIT
---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS stg_exceptions (
    exception_id      INTEGER PRIMARY KEY,
    source_table      TEXT NOT NULL,
    source_record_id  INTEGER NOT NULL,
    exception_type    TEXT NOT NULL,
    severity          TEXT NOT NULL,
    description       TEXT,
    timestamp         TEXT NOT NULL,
    rule_name         TEXT
);

CREATE TABLE IF NOT EXISTS stg_audit_log (
    audit_id          INTEGER PRIMARY KEY,
    staging_table     TEXT NOT NULL,
    raw_table         TEXT NOT NULL,
    raw_record_id     INTEGER NOT NULL,
    action            TEXT NOT NULL,
    timestamp         TEXT NOT NULL,
    rule_name         TEXT
);


---------------------------------------------------------------------------
-- MASTER DATA (CLEANED)
---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS stg_sites_clean (
    site_key          INTEGER PRIMARY KEY,
    site_id           INTEGER NOT NULL,
    site_code         TEXT NOT NULL,
    site_name         TEXT NOT NULL,
    region            TEXT,
    status            TEXT CHECK(status IN ('active','inactive'))
);

CREATE TABLE IF NOT EXISTS stg_items_clean (
    item_key          INTEGER PRIMARY KEY,
    item_id           INTEGER NOT NULL,
    item_sku          TEXT NOT NULL,
    item_name         TEXT NOT NULL,
    item_type         TEXT CHECK(item_type IN ('FG','WIP','RM')),
    uom               TEXT NOT NULL,
    status            TEXT CHECK(status IN ('active','inactive'))
);

CREATE TABLE IF NOT EXISTS stg_vendors_clean (
    vendor_key        INTEGER PRIMARY KEY,
    vendor_id         INTEGER NOT NULL,
    vendor_code       TEXT NOT NULL,
    vendor_name       TEXT NOT NULL,
    status            TEXT CHECK(status IN ('active','inactive'))
);

CREATE TABLE IF NOT EXISTS stg_customers_clean (
    customer_key      INTEGER PRIMARY KEY,
    customer_id       INTEGER NOT NULL,
    customer_code     TEXT NOT NULL,
    customer_name     TEXT NOT NULL,
    status            TEXT CHECK(status IN ('active','inactive'))
);

CREATE TABLE IF NOT EXISTS stg_machines_clean (
    machine_key       INTEGER PRIMARY KEY,
    machine_id        INTEGER NOT NULL,
    machine_code      TEXT NOT NULL,
    machine_name      TEXT NOT NULL,
    site_id           INTEGER NOT NULL,
    status            TEXT CHECK(status IN ('active','inactive'))
);

CREATE TABLE IF NOT EXISTS stg_operators_clean (
    operator_key      INTEGER PRIMARY KEY,
    operator_id       INTEGER NOT NULL,
    operator_code     TEXT NOT NULL,
    operator_name     TEXT NOT NULL,
    role              TEXT,
    site_id           INTEGER NOT NULL
);


---------------------------------------------------------------------------
-- TRANSACTIONAL DATA (CLEANED)
---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS stg_inventory_clean (
    inventory_key     INTEGER PRIMARY KEY,
    inventory_id      INTEGER NOT NULL,
    site_key          INTEGER NOT NULL,
    item_key          INTEGER NOT NULL,
    quantity_on_hand  REAL NOT NULL,
    location_code     TEXT,
    last_updated_at   TEXT,
    last_updated_by   TEXT
);

CREATE TABLE IF NOT EXISTS stg_inventory_txn_clean (
    txn_key           INTEGER PRIMARY KEY,
    txn_id            INTEGER NOT NULL,
    site_key          INTEGER NOT NULL,
    item_key          INTEGER NOT NULL,
    txn_type          TEXT NOT NULL,
    quantity          REAL NOT NULL,
    timestamp         TEXT NOT NULL,
    reference_id      INTEGER,
    notes             TEXT
);

CREATE TABLE IF NOT EXISTS stg_work_orders_clean (
    wo_key            INTEGER PRIMARY KEY,
    work_order_id     INTEGER NOT NULL,
    site_key          INTEGER NOT NULL,
    item_key          INTEGER NOT NULL,
    planned_quantity  REAL NOT NULL,
    scheduled_start   TEXT,
    scheduled_end     TEXT,
    status            TEXT,
    created_by        TEXT
);

CREATE TABLE IF NOT EXISTS stg_throughput_clean (
    throughput_key    INTEGER PRIMARY KEY,
    throughput_id     INTEGER NOT NULL,
    site_key          INTEGER NOT NULL,
    wo_key            INTEGER NOT NULL,
    machine_key       INTEGER NOT NULL,
    operator_key      INTEGER NOT NULL,
    units_produced    REAL NOT NULL,
    scrap_units       REAL,
    timestamp         TEXT NOT NULL,
    shift_code        TEXT
);

CREATE TABLE IF NOT EXISTS stg_scrap_clean (
    scrap_key         INTEGER PRIMARY KEY,
    scrap_id          INTEGER NOT NULL,
    site_key          INTEGER NOT NULL,
    item_key          INTEGER NOT NULL,
    quantity          REAL NOT NULL,
    reason            TEXT,
    timestamp         TEXT NOT NULL,
    operator_key      INTEGER
);


---------------------------------------------------------------------------
-- PROCUREMENT (CLEANED)
---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS stg_po_clean (
    po_key            INTEGER PRIMARY KEY,
    po_id             INTEGER NOT NULL,
    vendor_key        INTEGER NOT NULL,
    po_date           TEXT NOT NULL,
    status            TEXT,
    created_by        TEXT
);

CREATE TABLE IF NOT EXISTS stg_po_lines_clean (
    po_line_key       INTEGER PRIMARY KEY,
    po_line_id        INTEGER NOT NULL,
    po_key            INTEGER NOT NULL,
    item_key          INTEGER NOT NULL,
    ordered_quantity  REAL NOT NULL,
    uom               TEXT NOT NULL,
    notes             TEXT
);

CREATE TABLE IF NOT EXISTS stg_receipts_clean (
    receipt_key       INTEGER PRIMARY KEY,
    receipt_id        INTEGER NOT NULL,
    po_line_key       INTEGER NOT NULL,
    received_quantity REAL NOT NULL,
    timestamp         TEXT NOT NULL,
    received_by       TEXT
);


---------------------------------------------------------------------------
-- SALES (CLEANED)
---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS stg_customer_orders_clean (
    order_key         INTEGER PRIMARY KEY,
    order_id          INTEGER NOT NULL,
    customer_key      INTEGER NOT NULL,
    order_date        TEXT NOT NULL,
    required_date     TEXT,
    status            TEXT,
    created_by        TEXT
);

CREATE TABLE IF NOT EXISTS stg_customer_order_lines_clean (
    order_line_key    INTEGER PRIMARY KEY,
    order_line_id     INTEGER NOT NULL,
    order_key         INTEGER NOT NULL,
    item_key          INTEGER NOT NULL,
    ordered_quantity  REAL NOT NULL,
    uom               TEXT NOT NULL,
    notes             TEXT
);

CREATE TABLE IF NOT EXISTS stg_shipping_clean (
    shipment_key      INTEGER PRIMARY KEY,
    shipment_id       INTEGER NOT NULL,
    order_key         INTEGER NOT NULL,
    shipped_quantity  REAL NOT NULL,
    timestamp         TEXT NOT NULL,
    carrier           TEXT,
    tracking_number   TEXT
);


---------------------------------------------------------------------------
-- FINANCE (CLEANED)
---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS stg_ap_clean (
    ap_key            INTEGER PRIMARY KEY,
    ap_id             INTEGER NOT NULL,
    vendor_key        INTEGER NOT NULL,
    amount            REAL NOT NULL,
    due_date          TEXT,
    status            TEXT
);

CREATE TABLE IF NOT EXISTS stg_ar_clean (
    ar_key            INTEGER PRIMARY KEY,
    ar_id             INTEGER NOT NULL,
    customer_key      INTEGER NOT NULL,
    amount            REAL NOT NULL,
    due_date          TEXT,
    status            TEXT
);

CREATE TABLE IF NOT EXISTS stg_costing_clean (
    cost_key          INTEGER PRIMARY KEY,
    cost_id           INTEGER NOT NULL,
    item_key          INTEGER NOT NULL,
    site_key          INTEGER NOT NULL,
    standard_cost     REAL NOT NULL,
    last_updated_at   TEXT,
    updated_by        TEXT
);
