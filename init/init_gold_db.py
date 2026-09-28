import sqlite3
import os

DB_PATH = "gold_source.db"

def init_gold_db():
    # Deterministic: only create the Gold Source DB if it does not already exist
    if os.path.exists(DB_PATH):
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    schema = """
     -------------------------------------------------------------------------
    -- GOLD SOURCE: Clean, standardized, analytics-ready tables
    -- These tables represent the "single source of truth" after deterministic
    -- validation, normalization, and transformation of ERP raw data.
    -------------------------------------------------------------------------

    -------------------------------------------------------------------------
    -- DIMENSIONS (Master Data)
    -------------------------------------------------------------------------

    -- Dim Sites: normalized site reference table
    CREATE TABLE IF NOT EXISTS dim_sites (
        site_key       INTEGER PRIMARY KEY,
        site_id        INTEGER NOT NULL,
        site_code      TEXT NOT NULL,
        site_name      TEXT NOT NULL,
        region         TEXT,
        status         TEXT
    );

    -- Dim Items: normalized item reference table
    CREATE TABLE IF NOT EXISTS dim_items (
        item_key       INTEGER PRIMARY KEY,
        item_id        INTEGER NOT NULL,
        item_sku       TEXT NOT NULL,
        item_name      TEXT NOT NULL,
        item_type      TEXT,
        uom            TEXT,
        status         TEXT
    );

    -- Dim Vendors: normalized vendor reference table
    CREATE TABLE IF NOT EXISTS dim_vendors (
        vendor_key     INTEGER PRIMARY KEY,
        vendor_id      INTEGER NOT NULL,
        vendor_code    TEXT NOT NULL,
        vendor_name    TEXT NOT NULL,
        status         TEXT
    );

    -- Dim Customers: normalized customer reference table
    CREATE TABLE IF NOT EXISTS dim_customers (
        customer_key   INTEGER PRIMARY KEY,
        customer_id    INTEGER NOT NULL,
        customer_code  TEXT NOT NULL,
        customer_name  TEXT NOT NULL,
        status         TEXT
    );

    -- Dim Machines: normalized machine reference table
    CREATE TABLE IF NOT EXISTS dim_machines (
        machine_key    INTEGER PRIMARY KEY,
        machine_id     INTEGER NOT NULL,
        machine_code   TEXT NOT NULL,
        machine_name   TEXT NOT NULL,
        site_id        INTEGER,
        status         TEXT
    );

    -- Dim Operators: normalized operator reference table
    CREATE TABLE IF NOT EXISTS dim_operators (
        operator_key   INTEGER PRIMARY KEY,
        operator_id    INTEGER NOT NULL,
        operator_code  TEXT NOT NULL,
        operator_name  TEXT NOT NULL,
        role           TEXT,
        site_id        INTEGER
    );

    -------------------------------------------------------------------------
    -- FACT TABLES (Cleaned transactional data)
    -------------------------------------------------------------------------

    -- Fact Purchase Orders: PO header-level facts
    CREATE TABLE IF NOT EXISTS fact_purchase_orders (
        po_key         INTEGER PRIMARY KEY,
        po_id          INTEGER NOT NULL,
        vendor_key     INTEGER NOT NULL,
        po_date        TEXT NOT NULL,
        status         TEXT,
        created_by     TEXT
    );

    -- Fact PO Lines: line-level purchasing facts
    CREATE TABLE IF NOT EXISTS fact_po_lines (
        po_line_key    INTEGER PRIMARY KEY,
        po_line_id     INTEGER NOT NULL,
        po_key         INTEGER NOT NULL,
        item_key       INTEGER NOT NULL,
        ordered_quantity REAL NOT NULL,
        uom            TEXT,
        notes          TEXT
    );

    -- Fact Receipts: inbound material receipts
    CREATE TABLE IF NOT EXISTS fact_receipts (
        receipt_key    INTEGER PRIMARY KEY,
        receipt_id     INTEGER NOT NULL,
        po_line_key    INTEGER NOT NULL,
        received_quantity REAL NOT NULL,
        timestamp      TEXT NOT NULL,
        received_by    TEXT
    );

    -- Fact Inventory Balances: cleaned inventory quantities
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

     -- Fact Inventory Transactions: cleaned inventory movements
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

    -- Fact BOM: cleaned bill of materials structure
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

    -- Fact Routing: cleaned routing steps
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

    -- Fact Work Orders: cleaned production orders
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

    -- Fact Throughput: cleaned production output
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

    -- Fact Scrap: cleaned scrap records
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

    -- Fact Customer Orders: cleaned sales orders
    CREATE TABLE IF NOT EXISTS fact_customer_orders (
        order_key      INTEGER PRIMARY KEY,
        order_id       INTEGER NOT NULL,
        customer_key   INTEGER NOT NULL,
        order_date     TEXT NOT NULL,
        required_date  TEXT,
        status         TEXT,
        created_by     TEXT
    );

    -- Fact Customer Order Lines: cleaned sales order lines
    CREATE TABLE IF NOT EXISTS fact_customer_order_lines (
        order_line_key INTEGER PRIMARY KEY,
        order_line_id  INTEGER NOT NULL,
        order_key      INTEGER NOT NULL,
        item_key       INTEGER NOT NULL,
        ordered_quantity REAL NOT NULL,
        uom            TEXT,
        notes          TEXT
    );

    -- Fact Shipments: cleaned outbound shipments
    CREATE TABLE IF NOT EXISTS fact_shipments (
        shipment_key   INTEGER PRIMARY KEY,
        shipment_id    INTEGER NOT NULL,
        order_key      INTEGER NOT NULL,
        shipped_quantity REAL NOT NULL,
        timestamp      TEXT NOT NULL,
        carrier        TEXT,
        tracking_number TEXT
    );

    -------------------------------------------------------------------------
    -- FINANCE FACTS
    -------------------------------------------------------------------------

    -- Fact AP: cleaned accounts payable
    CREATE TABLE IF NOT EXISTS fact_ap (
        ap_key         INTEGER PRIMARY KEY,
        ap_id          INTEGER NOT NULL,
        vendor_key     INTEGER NOT NULL,
        amount         REAL NOT NULL,
        due_date       TEXT,
        status         TEXT
    );

    -- Fact AR: cleaned accounts receivable
    CREATE TABLE IF NOT EXISTS fact_ar (
        ar_key         INTEGER PRIMARY KEY,
        ar_id          INTEGER NOT NULL,
        customer_key   INTEGER NOT NULL,
        amount         REAL NOT NULL,
        due_date       TEXT,
        status         TEXT
    );

     -- Fact Costing: cleaned standard cost records
    CREATE TABLE IF NOT EXISTS fact_costing (
        cost_key       INTEGER PRIMARY KEY,
        cost_id        INTEGER NOT NULL,
        item_key       INTEGER NOT NULL,
        site_key       INTEGER NOT NULL,
        standard_cost  REAL NOT NULL,
        last_updated_at TEXT,
        updated_by     TEXT
    );

    -------------------------------------------------------------------------
    -- GOVERNANCE
    -------------------------------------------------------------------------

    -- Fact Exceptions: cleaned exception log for deterministic pipeline
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

    -- Fact Audit Log: cleaned audit records
    CREATE TABLE IF NOT EXISTS fact_audit_log (
        audit_key      INTEGER PRIMARY KEY,
        audit_id       INTEGER NOT NULL,
        table_name     TEXT NOT NULL,
        record_id      INTEGER NOT NULL,
        action         TEXT NOT NULL,
        timestamp      TEXT NOT NULL,
        user           TEXT
    );
    """

    cursor.executescript(schema)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_gold_db()