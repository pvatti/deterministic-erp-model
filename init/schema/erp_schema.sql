---------------------------------------------------------------------------
-- ERP SCHEMA (RAW LAYER)
-- This file defines the full raw ERP schema used before deterministic
-- transformation into the Gold Source layer.
---------------------------------------------------------------------------


---------------------------------------------------------------------------
-- MASTER DATA
---------------------------------------------------------------------------

-- Sites: physical manufacturing or distribution locations
CREATE TABLE IF NOT EXISTS sites (
    site_id        INTEGER PRIMARY KEY,
    site_code      TEXT NOT NULL UNIQUE,
    site_name      TEXT NOT NULL,
    region         TEXT,
    status         TEXT CHECK(status IN ('active','inactive'))
);

-- Items: finished goods, WIP, raw materials
CREATE TABLE IF NOT EXISTS items (
    item_id        INTEGER PRIMARY KEY,
    item_sku       TEXT NOT NULL UNIQUE,
    item_name      TEXT NOT NULL,
    item_type      TEXT CHECK(item_type IN ('FG','WIP','RM')),
    uom            TEXT NOT NULL,
    status         TEXT CHECK(status IN ('active','inactive'))
);

-- Machines: equipment used in production routing steps
CREATE TABLE IF NOT EXISTS machines (
    machine_id     INTEGER PRIMARY KEY,
    site_id        INTEGER NOT NULL,
    machine_code   TEXT NOT NULL,
    machine_name   TEXT NOT NULL,
    status         TEXT CHECK(status IN ('active','inactive')),
    FOREIGN KEY (site_id) REFERENCES sites(site_id)
);

-- Operators: people running machines or performing production work
CREATE TABLE IF NOT EXISTS operators (
    operator_id    INTEGER PRIMARY KEY,
    site_id        INTEGER NOT NULL,
    operator_code  TEXT NOT NULL,
    operator_name  TEXT NOT NULL,
    role           TEXT,
    FOREIGN KEY (site_id) REFERENCES sites(site_id)
);

-- Vendors: suppliers for purchasing raw materials or services
CREATE TABLE IF NOT EXISTS vendors (
    vendor_id      INTEGER PRIMARY KEY,
    vendor_code    TEXT NOT NULL UNIQUE,
    vendor_name    TEXT NOT NULL,
    status         TEXT CHECK(status IN ('active','inactive'))
);

-- Customers: buyers of finished goods
CREATE TABLE IF NOT EXISTS customers (
    customer_id    INTEGER PRIMARY KEY,
    customer_code  TEXT NOT NULL UNIQUE,
    customer_name  TEXT NOT NULL,
    status         TEXT CHECK(status IN ('active','inactive'))
);


---------------------------------------------------------------------------
-- PROCUREMENT
---------------------------------------------------------------------------

-- Purchase Orders: header-level purchasing documents
CREATE TABLE IF NOT EXISTS purchase_orders_raw (
    po_id          INTEGER PRIMARY KEY,
    vendor_id      INTEGER NOT NULL,
    po_date        TEXT NOT NULL,
    status         TEXT,
    created_by     TEXT,
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

-- PO Lines: line-level detail for items ordered
CREATE TABLE IF NOT EXISTS po_lines_raw (
    po_line_id     INTEGER PRIMARY KEY,
    po_id          INTEGER NOT NULL,
    item_id        INTEGER NOT NULL,
    ordered_quantity REAL NOT NULL,
    uom            TEXT NOT NULL,
    notes          TEXT,
    FOREIGN KEY (po_id) REFERENCES purchase_orders_raw(po_id),
    FOREIGN KEY (item_id) REFERENCES items(item_id)
);

-- Receipts: inbound material receipts against PO lines
CREATE TABLE IF NOT EXISTS receipts_raw (
    receipt_id     INTEGER PRIMARY KEY,
    po_line_id     INTEGER NOT NULL,
    received_quantity REAL NOT NULL,
    timestamp      TEXT NOT NULL,
    received_by    TEXT,
    FOREIGN KEY (po_line_id) REFERENCES po_lines_raw(po_line_id)
);


---------------------------------------------------------------------------
-- INVENTORY
---------------------------------------------------------------------------

-- Inventory: current quantity on hand per site/item/location
CREATE TABLE IF NOT EXISTS inventory_raw (
    inventory_id   INTEGER PRIMARY KEY,
    site_id        INTEGER NOT NULL,
    item_id        INTEGER NOT NULL,
    quantity_on_hand REAL NOT NULL,
    location_code  TEXT,
    last_updated_at TEXT,
    last_updated_by TEXT,
    notes          TEXT,
    FOREIGN KEY (site_id) REFERENCES sites(site_id),
    FOREIGN KEY (item_id) REFERENCES items(item_id)
);

-- Inventory Transactions: receipts, issues, adjustments
CREATE TABLE IF NOT EXISTS inventory_transactions_raw (
    txn_id         INTEGER PRIMARY KEY,
    site_id        INTEGER NOT NULL,
    item_id        INTEGER NOT NULL,
    txn_type       TEXT NOT NULL,
    quantity       REAL NOT NULL,
    timestamp      TEXT NOT NULL,
    reference_id   INTEGER,
    notes          TEXT,
    FOREIGN KEY (site_id) REFERENCES sites(site_id),
    FOREIGN KEY (item_id) REFERENCES items(item_id)
);

-- BOM: bill of materials defining component relationships
CREATE TABLE IF NOT EXISTS bom_raw (
    bom_id         INTEGER PRIMARY KEY,
    item_id        INTEGER NOT NULL,
    component_item_id INTEGER NOT NULL,
    quantity_per   REAL NOT NULL,
    site_id        INTEGER NOT NULL,
    version        TEXT,
    effective_from TEXT,
    effective_to   TEXT,
    updated_by     TEXT,
    notes          TEXT,
    FOREIGN KEY (item_id) REFERENCES items(item_id),
    FOREIGN KEY (component_item_id) REFERENCES items(item_id),
    FOREIGN KEY (site_id) REFERENCES sites(site_id)
);


---------------------------------------------------------------------------
-- PRODUCTION
---------------------------------------------------------------------------

-- Routing: ordered steps required to manufacture an item
CREATE TABLE IF NOT EXISTS routing_raw (
    routing_id     INTEGER PRIMARY KEY,
    item_id        INTEGER NOT NULL,
    site_id        INTEGER NOT NULL,
    step_number    INTEGER NOT NULL,
    operation_code TEXT NOT NULL,
    machine_id     INTEGER,
    standard_duration_minutes REAL,
    updated_by     TEXT,
    notes          TEXT,
    FOREIGN KEY (item_id) REFERENCES items(item_id),
    FOREIGN KEY (site_id) REFERENCES sites(site_id),
    FOREIGN KEY (machine_id) REFERENCES machines(machine_id)
);

-- Work Orders: planned production jobs
CREATE TABLE IF NOT EXISTS work_orders_raw (
    work_order_id  INTEGER PRIMARY KEY,
    site_id        INTEGER NOT NULL,
    item_id        INTEGER NOT NULL,
    planned_quantity REAL NOT NULL,
    scheduled_start TEXT,
    scheduled_end   TEXT,
    status         TEXT,
    created_by     TEXT,
    FOREIGN KEY (site_id) REFERENCES sites(site_id),
    FOREIGN KEY (item_id) REFERENCES items(item_id)
);

-- Throughput: actual production output per machine/operator/WO
CREATE TABLE IF NOT EXISTS throughput_raw (
    throughput_id  INTEGER PRIMARY KEY,
    site_id        INTEGER NOT NULL,
    work_order_id  INTEGER NOT NULL,
    machine_id     INTEGER NOT NULL,
    operator_id    INTEGER NOT NULL,
    units_produced REAL NOT NULL,
    scrap_units    REAL,
    timestamp      TEXT NOT NULL,
    shift_code     TEXT,
    notes          TEXT,
    FOREIGN KEY (site_id) REFERENCES sites(site_id),
    FOREIGN KEY (work_order_id) REFERENCES work_orders_raw(work_order_id),
    FOREIGN KEY (machine_id) REFERENCES machines(machine_id),
    FOREIGN KEY (operator_id) REFERENCES operators(operator_id)
);

-- Scrap: recorded losses during production
CREATE TABLE IF NOT EXISTS scrap_raw (
    scrap_id       INTEGER PRIMARY KEY,
    site_id        INTEGER NOT NULL,
    item_id        INTEGER NOT NULL,
    quantity       REAL NOT NULL,
    reason         TEXT,
    timestamp      TEXT NOT NULL,
    operator_id    INTEGER,
    FOREIGN KEY (site_id) REFERENCES sites(site_id),
    FOREIGN KEY (item_id) REFERENCES items(item_id),
    FOREIGN KEY (operator_id) REFERENCES operators(operator_id)
);


---------------------------------------------------------------------------
-- SALES
---------------------------------------------------------------------------

-- Customer Orders: header-level sales orders
CREATE TABLE IF NOT EXISTS customer_orders_raw (
    order_id       INTEGER PRIMARY KEY,
    customer_id    INTEGER NOT NULL,
    order_date     TEXT NOT NULL,
    required_date  TEXT,
    status         TEXT,
    created_by     TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Customer Order Lines: item-level sales order detail
CREATE TABLE IF NOT EXISTS customer_order_lines_raw (
    order_line_id  INTEGER PRIMARY KEY,
    order_id       INTEGER NOT NULL,
    item_id        INTEGER NOT NULL,
    ordered_quantity REAL NOT NULL,
    uom            TEXT NOT NULL,
    notes          TEXT,
    FOREIGN KEY (order_id) REFERENCES customer_orders_raw(order_id),
    FOREIGN KEY (item_id) REFERENCES items(item_id)
);

-- Shipping: outbound shipments fulfilling customer orders
CREATE TABLE IF NOT EXISTS shipping_raw (
    shipment_id    INTEGER PRIMARY KEY,
    order_id       INTEGER NOT NULL,
    shipped_quantity REAL NOT NULL,
    timestamp      TEXT NOT NULL,
    carrier        TEXT,
    tracking_number TEXT,
    FOREIGN KEY (order_id) REFERENCES customer_orders_raw(order_id)
);


---------------------------------------------------------------------------
-- FINANCE
---------------------------------------------------------------------------

-- GL Accounts: chart of accounts
CREATE TABLE IF NOT EXISTS gl_accounts (
    gl_id          INTEGER PRIMARY KEY,
    gl_code        TEXT NOT NULL UNIQUE,
    gl_name        TEXT NOT NULL,
    gl_type        TEXT
);

-- Accounts Payable: vendor invoices
CREATE TABLE IF NOT EXISTS ap_raw (
    ap_id          INTEGER PRIMARY KEY,
    vendor_id      INTEGER NOT NULL,
    amount         REAL NOT NULL,
    due_date       TEXT,
    status         TEXT,
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

-- Accounts Receivable: customer invoices
CREATE TABLE IF NOT EXISTS ar_raw (
    ar_id          INTEGER PRIMARY KEY,
    customer_id    INTEGER NOT NULL,
    amount         REAL NOT NULL,
    due_date       TEXT,
    status         TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Costing: standard cost per item per site
CREATE TABLE IF NOT EXISTS costing_raw (
    cost_id        INTEGER PRIMARY KEY,
    item_id        INTEGER NOT NULL,
    site_id        INTEGER NOT NULL,
    standard_cost  REAL NOT NULL,
    last_updated_at TEXT,
    updated_by     TEXT,
    FOREIGN KEY (item_id) REFERENCES items(item_id),
    FOREIGN KEY (site_id) REFERENCES sites(site_id)
);


---------------------------------------------------------------------------
-- GOVERNANCE
---------------------------------------------------------------------------

-- Exceptions: data quality issues detected during ingestion
CREATE TABLE IF NOT EXISTS exceptions_raw (
    exception_id   INTEGER PRIMARY KEY,
    site_id        INTEGER,
    source_table   TEXT NOT NULL,
    source_record_id INTEGER NOT NULL,
    exception_type TEXT NOT NULL,
    description    TEXT,
    severity       TEXT,
    timestamp      TEXT NOT NULL,
    reported_by    TEXT,
    FOREIGN KEY (site_id) REFERENCES sites(site_id)
);

-- Audit Log: tracks changes for governance and traceability
CREATE TABLE IF NOT EXISTS audit_log_raw (
    audit_id       INTEGER PRIMARY KEY,
    table_name     TEXT NOT NULL,
    record_id      INTEGER NOT NULL,
    action         TEXT NOT NULL,
    timestamp      TEXT NOT NULL,
    user           TEXT
);
