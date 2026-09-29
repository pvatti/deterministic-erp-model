---------------------------------------------------------------------------
-- GOLD SOURCE SCHEMA
-- Clean, standardized, analytics-ready tables produced by deterministic
-- transformation of ERP raw data. This is the "single source of truth."
---------------------------------------------------------------------------


---------------------------------------------------------------------------
-- DIMENSIONS (Master Data)
---------------------------------------------------------------------------

-- Sites (normalized)
CREATE TABLE IF NOT EXISTS dim_sites (
    site_key       INTEGER PRIMARY KEY,
    site_id        INTEGER NOT NULL,
    site_code      TEXT NOT NULL,
    site_name      TEXT NOT NULL,
    region         TEXT,
    status         TEXT
);

-- Items (normalized)
CREATE TABLE IF NOT EXISTS dim_items (
    item_key       INTEGER PRIMARY KEY,
    item_id        INTEGER NOT NULL,
    item_sku       TEXT NOT NULL,
    item_name      TEXT NOT NULL,
    item_type      TEXT,
    uom            TEXT,
    status         TEXT
);

-- Vendors (normalized)
CREATE TABLE IF NOT EXISTS dim_vendors (
    vendor_key     INTEGER PRIMARY KEY,
    vendor_id      INTEGER NOT NULL,
    vendor_code    TEXT NOT NULL,
    vendor_name    TEXT NOT NULL,
    status         TEXT
);

-- Customers (normalized)
CREATE TABLE IF NOT EXISTS dim_customers (
    customer_key   INTEGER PRIMARY KEY,
    customer_id    INTEGER NOT NULL,
    customer_code  TEXT NOT NULL,
    customer_name  TEXT NOT NULL,
    status         TEXT
);

-- Machines (normalized)
CREATE TABLE IF NOT EXISTS dim_machines (
    machine_key    INTEGER PRIMARY KEY,
    machine_id     INTEGER NOT NULL,
    machine_code   TEXT NOT NULL,
    machine_name   TEXT NOT NULL,
    site_id        INTEGER,
    status         TEXT
);

-- Operators (normalized)
CREATE TABLE IF NOT EXISTS dim_operators (
    operator_key   INTEGER PRIMARY KEY,
    operator_id    INTEGER NOT NULL,
    operator_code  TEXT NOT NULL,
    operator_name  TEXT NOT NULL,
    role           TEXT,
    site_id        INTEGER
);


---------------------------------------------------------------------------
-- FACT TABLES (Transactional Data)
---------------------------------------------------------------------------

-- Purchase Orders (header)
CREATE TABLE IF NOT EXISTS fact_purchase_orders (
    po_key         INTEGER PRIMARY KEY,
    po_id          INTEGER NOT NULL,
    vendor_key     INTEGER NOT NULL,
    po_date        TEXT NOT NULL,
    status         TEXT,
    created_by     TEXT
);

-- Purchase Order Lines
CREATE TABLE IF NOT EXISTS fact_po_lines (
    po_line_key    INTEGER PRIMARY KEY,
    po_line_id     INTEGER NOT NULL,
    po_key         INTEGER NOT NULL,
    item_key       INTEGER NOT NULL,
    ordered_quantity REAL NOT NULL,
    uom            TEXT,
    notes          TEXT
);

-- Receipts
CREATE TABLE IF NOT EXISTS fact_receipts (
    receipt_key    INTEGER PRIMARY KEY,
    receipt_id     INTEGER NOT NULL,
    po_line_key    INTEGER NOT NULL,
    received_quantity REAL NOT NULL,
    timestamp      TEXT NOT NULL,
    received_by    TEXT
);

-- Inventory Balances
CREATE TABLE IF NOT EXISTS fact_inventory (
    inventory_key  INTEGER PRIMARY KEY,
    inventory_id   INTEGER NOT NULL,
    site_key       INTEGER NOT NULL,
    item_key       INTEGER NOT NULL,
    quantity_on_hand REAL NOT NULL,
    location_code  TEXT,
    last_updated_at TEXT,
    last_updated_by TEXT
);

-- Inventory Transactions
CREATE TABLE IF NOT EXISTS fact_inventory_transactions (
    txn_key        INTEGER PRIMARY KEY,
    txn_id         INTEGER NOT NULL,
    site_key       INTEGER NOT NULL,
    item_key       INTEGER NOT NULL,
    txn_type       TEXT NOT NULL,
    quantity       REAL NOT NULL,
    timestamp      TEXT NOT NULL,
    reference_id   INTEGER,
    notes          TEXT
);

-- Bill of Materials
CREATE TABLE IF NOT EXISTS fact_bom (
    bom_key        INTEGER PRIMARY KEY,
    bom_id         INTEGER NOT NULL,
    parent_item_key INTEGER NOT NULL,
    component_item_key INTEGER NOT NULL,
    quantity_per   REAL NOT NULL,
    site_key       INTEGER NOT NULL,
    version        TEXT,
    effective_from TEXT,
    effective_to   TEXT
);

-- Routing
CREATE TABLE IF NOT EXISTS fact_routing (
    routing_key    INTEGER PRIMARY KEY,
    routing_id     INTEGER NOT NULL,
    item_key       INTEGER NOT NULL,
    site_key       INTEGER NOT NULL,
    step_number    INTEGER NOT NULL,
    operation_code TEXT NOT NULL,
    machine_key    INTEGER,
    standard_duration_minutes REAL
);

-- Work Orders
CREATE TABLE IF NOT EXISTS fact_work_orders (
    wo_key         INTEGER PRIMARY KEY,
    work_order_id  INTEGER NOT NULL,
    site_key       INTEGER NOT NULL,
    item_key       INTEGER NOT NULL,
    planned_quantity REAL NOT NULL,
    scheduled_start TEXT,
    scheduled_end   TEXT,
    status         TEXT,
    created_by     TEXT
);

-- Throughput
CREATE TABLE IF NOT EXISTS fact_throughput (
    throughput_key INTEGER PRIMARY KEY,
    throughput_id  INTEGER NOT NULL,
    site_key       INTEGER NOT NULL,
    wo_key         INTEGER NOT NULL,
    machine_key    INTEGER NOT NULL,
    operator_key   INTEGER NOT NULL,
    units_produced REAL NOT NULL,
    scrap_units    REAL,
    timestamp      TEXT NOT NULL,
    shift_code     TEXT
);

-- Scrap
CREATE TABLE IF NOT EXISTS fact_scrap (
    scrap_key      INTEGER PRIMARY KEY,
    scrap_id       INTEGER NOT NULL,
    site_key       INTEGER NOT NULL,
    item_key       INTEGER NOT NULL,
    quantity       REAL NOT NULL,
    reason         TEXT,
    timestamp      TEXT NOT NULL,
    operator_key   INTEGER
);

-- Customer Orders (header)
CREATE TABLE IF NOT EXISTS fact_customer_orders (
    order_key      INTEGER PRIMARY KEY,
    order_id       INTEGER NOT NULL,
    customer_key   INTEGER NOT NULL,
    order_date     TEXT NOT NULL,
    required_date  TEXT,
    status         TEXT,
    created_by     TEXT
);

-- Customer Order Lines
CREATE TABLE IF NOT EXISTS fact_customer_order_lines (
    order_line_key INTEGER PRIMARY KEY,
    order_line_id  INTEGER NOT NULL,
    order_key      INTEGER NOT NULL,
    item_key       INTEGER NOT NULL,
    ordered_quantity REAL NOT NULL,
    uom            TEXT,
    notes          TEXT
);

-- Shipments
CREATE TABLE IF NOT EXISTS fact_shipments (
    shipment_key   INTEGER PRIMARY KEY,
    shipment_id    INTEGER NOT NULL,
    order_key      INTEGER NOT NULL,
    shipped_quantity REAL NOT NULL,
    timestamp      TEXT NOT NULL,
    carrier        TEXT,
    tracking_number TEXT
);


---------------------------------------------------------------------------
-- FINANCE
---------------------------------------------------------------------------

-- Accounts Payable
CREATE TABLE IF NOT EXISTS fact_ap (
    ap_key         INTEGER PRIMARY KEY,
    ap_id          INTEGER NOT NULL,
    vendor_key     INTEGER NOT NULL,
    amount         REAL NOT NULL,
    due_date       TEXT,
    status         TEXT
);

-- Accounts Receivable
CREATE TABLE IF NOT EXISTS fact_ar (
    ar_key         INTEGER PRIMARY KEY,
    ar_id          INTEGER NOT NULL,
    customer_key   INTEGER NOT NULL,
    amount         REAL NOT NULL,
    due_date       TEXT,
    status         TEXT
);

-- Costing
CREATE TABLE IF NOT EXISTS fact_costing (
    cost_key       INTEGER PRIMARY KEY,
    cost_id        INTEGER NOT NULL,
    item_key       INTEGER NOT NULL,
    site_key       INTEGER NOT NULL,
    standard_cost  REAL NOT NULL,
    last_updated_at TEXT,
    updated_by     TEXT
);


---------------------------------------------------------------------------
-- GOVERNANCE
---------------------------------------------------------------------------

-- Exceptions (cleaned)
CREATE TABLE IF NOT EXISTS fact_exceptions (
    exception_key  INTEGER PRIMARY KEY,
    exception_id   INTEGER NOT NULL,
    site_key       INTEGER,
    source_table   TEXT NOT NULL,
    source_record_id INTEGER NOT NULL,
    exception_type TEXT NOT NULL,
    description    TEXT,
    severity       TEXT,
    timestamp      TEXT NOT NULL,
    reported_by    TEXT
);

-- Audit Log (cleaned)
CREATE TABLE IF NOT EXISTS fact_audit_log (
    audit_key      INTEGER PRIMARY KEY,
    audit_id       INTEGER NOT NULL,
    table_name     TEXT NOT NULL,
    record_id      INTEGER NOT NULL,
    action         TEXT NOT NULL,
    timestamp      TEXT NOT NULL,
    user           TEXT
);
