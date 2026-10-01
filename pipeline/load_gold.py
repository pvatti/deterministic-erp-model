import sqlite3
import os


# ---------------------------------------------------------------------------
# GOLD LOADERS
# ---------------------------------------------------------------------------

def load_dim_sites(stg, gold):
    rows = stg.execute("SELECT site_key, site_id, site_code, site_name, region, status FROM stg_sites_clean;").fetchall()
    for r in rows:
        gold.execute("""
            INSERT INTO dim_sites (site_key, site_id, site_code, site_name, region, status)
            VALUES (?, ?, ?, ?, ?, ?);
        """, r)


def load_dim_items(stg, gold):
    rows = stg.execute("SELECT item_key, item_id, item_sku, item_name, item_type, uom, status FROM stg_items_clean;").fetchall()
    for r in rows:
        gold.execute("""
            INSERT INTO dim_items (item_key, item_id, item_sku, item_name, item_type, uom, status)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """, r)


def load_dim_vendors(stg, gold):
    rows = stg.execute("SELECT vendor_key, vendor_id, vendor_code, vendor_name, status FROM stg_vendors_clean;").fetchall()
    for r in rows:
        gold.execute("""
            INSERT INTO dim_vendors (vendor_key, vendor_id, vendor_code, vendor_name, status)
            VALUES (?, ?, ?, ?, ?);
        """, r)


def load_dim_customers(stg, gold):
    rows = stg.execute("SELECT customer_key, customer_id, customer_code, customer_name, status FROM stg_customers_clean;").fetchall()
    for r in rows:
        gold.execute("""
            INSERT INTO dim_customers (customer_key, customer_id, customer_code, customer_name, status)
            VALUES (?, ?, ?, ?, ?);
        """, r)


def load_dim_machines(stg, gold):
    rows = stg.execute("SELECT machine_key, machine_id, machine_code, machine_name, site_id, status FROM stg_machines_clean;").fetchall()
    for r in rows:
        gold.execute("""
            INSERT INTO dim_machines (machine_key, machine_id, machine_code, machine_name, site_id, status)
            VALUES (?, ?, ?, ?, ?, ?);
        """, r)


def load_dim_operators(stg, gold):
    rows = stg.execute("SELECT operator_key, operator_id, operator_code, operator_name, role, site_id FROM stg_operators_clean;").fetchall()
    for r in rows:
        gold.execute("""
            INSERT INTO dim_operators (operator_key, operator_id, operator_code, operator_name, role, site_id)
            VALUES (?, ?, ?, ?, ?, ?);
        """, r)


# ---------------------------------------------------------------------------
# FACT LOADERS
# ---------------------------------------------------------------------------

def load_fact_inventory(stg, gold):
    rows = stg.execute("""
        SELECT inventory_key, inventory_id, site_key, item_key,
               quantity_on_hand, location_code, last_updated_at, last_updated_by
        FROM stg_inventory_clean;
    """).fetchall()

    for r in rows:
        gold.execute("""
            INSERT INTO fact_inventory (
                inventory_key, inventory_id, site_key, item_key,
                quantity_on_hand, location_code, last_updated_at, last_updated_by
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """, r)


def load_fact_inventory_txn(stg, gold):
    rows = stg.execute("""
        SELECT txn_key, txn_id, site_key, item_key, txn_type,
               quantity, timestamp, reference_id, notes
        FROM stg_inventory_txn_clean;
    """).fetchall()

    for r in rows:
        gold.execute("""
            INSERT INTO fact_inventory_transactions (
                txn_key, txn_id, site_key, item_key, txn_type,
                quantity, timestamp, reference_id, notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, r)


def load_fact_work_orders(stg, gold):
    rows = stg.execute("""
        SELECT wo_key, work_order_id, site_key, item_key,
               planned_quantity, scheduled_start, scheduled_end,
               status, created_by
        FROM stg_work_orders_clean;
    """).fetchall()

    for r in rows:
        gold.execute("""
            INSERT INTO fact_work_orders (
                wo_key, work_order_id, site_key, item_key,
                planned_quantity, scheduled_start, scheduled_end,
                status, created_by
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, r)


def load_fact_throughput(stg, gold):
    rows = stg.execute("""
        SELECT throughput_key, throughput_id, site_key, wo_key,
               machine_key, operator_key, units_produced,
               scrap_units, timestamp, shift_code
        FROM stg_throughput_clean;
    """).fetchall()

    for r in rows:
        gold.execute("""
            INSERT INTO fact_throughput (
                throughput_key, throughput_id, site_key, wo_key,
                machine_key, operator_key, units_produced,
                scrap_units, timestamp, shift_code
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, r)


def load_fact_scrap(stg, gold):
    rows = stg.execute("""
        SELECT scrap_key, scrap_id, site_key, item_key,
               quantity, reason, timestamp, operator_key
        FROM stg_scrap_clean;
    """).fetchall()

    for r in rows:
        gold.execute("""
            INSERT INTO fact_scrap (
                scrap_key, scrap_id, site_key, item_key,
                quantity, reason, timestamp, operator_key
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """, r)


def load_fact_po(stg, gold):
    rows = stg.execute("""
        SELECT po_key, po_id, vendor_key, po_date, status, created_by
        FROM stg_po_clean;
    """).fetchall()

    for r in rows:
        gold.execute("""
            INSERT INTO fact_purchase_orders (
                po_key, po_id, vendor_key, po_date, status, created_by
            )
            VALUES (?, ?, ?, ?, ?, ?);
        """, r)


def load_fact_po_lines(stg, gold):
    rows = stg.execute("""
        SELECT po_line_key, po_line_id, po_key, item_key,
               ordered_quantity, uom, notes
        FROM stg_po_lines_clean;
    """).fetchall()

    for r in rows:
        gold.execute("""
            INSERT INTO fact_po_lines (
                po_line_key, po_line_id, po_key, item_key,
                ordered_quantity, uom, notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """, r)


def load_fact_receipts(stg, gold):
    rows = stg.execute("""
        SELECT receipt_key, receipt_id, po_line_key,
               received_quantity, timestamp, received_by
        FROM stg_receipts_clean;
    """).fetchall()

    for r in rows:
        gold.execute("""
            INSERT INTO fact_receipts (
                receipt_key, receipt_id, po_line_key,
                received_quantity, timestamp, received_by
            )
            VALUES (?, ?, ?, ?, ?, ?);
        """, r)


def load_fact_customer_orders(stg, gold):
    rows = stg.execute("""
        SELECT order_key, order_id, customer_key,
               order_date, required_date, status, created_by
        FROM stg_customer_orders_clean;
    """).fetchall()

    for r in rows:
        gold.execute("""
            INSERT INTO fact_customer_orders (
                order_key, order_id, customer_key,
                order_date, required_date, status, created_by
            )
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """, r)


def load_fact_customer_order_lines(stg, gold):
    rows = stg.execute("""
        SELECT order_line_key, order_line_id, order_key,
               item_key, ordered_quantity, uom, notes
        FROM stg_customer_order_lines_clean;
    """).fetchall()

    for r in rows:
        gold.execute("""
            INSERT INTO fact_customer_order_lines (
                order_line_key, order_line_id, order_key,
                item_key, ordered_quantity, uom, notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """, r)


def load_fact_shipping(stg, gold):
    rows = stg.execute("""
        SELECT shipment_key, shipment_id, order_key,
               shipped_quantity, timestamp, carrier, tracking_number
        FROM stg_shipping_clean;
    """).fetchall()

    for r in rows:
        gold.execute("""
            INSERT INTO fact_shipping (
                shipment_key, shipment_id, order_key,
                shipped_quantity, timestamp, carrier, tracking_number
            )
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """, r)


def load_fact_ap(stg, gold):
    rows = stg.execute("""
        SELECT ap_key, ap_id, vendor_key, amount, due_date, status
        FROM stg_ap_clean;
    """).fetchall()

    for r in rows:
        gold.execute("""
            INSERT INTO fact_ap (
                ap_key, ap_id, vendor_key, amount, due_date, status
            )
            VALUES (?, ?, ?, ?, ?, ?);
        """, r)


def load_fact_ar(stg, gold):
    rows = stg.execute("""
        SELECT ar_key, ar_id, customer_key, amount, due_date, status
        FROM stg_ar_clean;
    """).fetchall()

    for r in rows:
        gold.execute("""
            INSERT INTO fact_ar (
                ar_key, ar_id, customer_key, amount, due_date, status
            )
            VALUES (?, ?, ?, ?, ?, ?);
        """, r)


def load_fact_costing(stg, gold):
    rows = stg.execute("""
        SELECT cost_key, cost_id, item_key, site_key,
               standard_cost, last_updated_at, updated_by
        FROM stg_costing_clean;
    """).fetchall()

    for r in rows:
        gold.execute("""
            INSERT INTO fact_costing (
                cost_key, cost_id, item_key, site_key,
                standard_cost, last_updated_at, updated_by
            )
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """, r)


# ---------------------------------------------------------------------------
# MAIN GOLD LOADER
# ---------------------------------------------------------------------------

def load_gold():
    if os.path.exists("data/gold.db"):
        print("Removing existing GOLD database...")
        os.remove("data/gold.db")

    conn = sqlite3.connect("data/gold.db")
    gold = conn.cursor()

    conn.execute("ATTACH DATABASE 'data/staging.db' AS stg;")
    stg = conn.cursor()

    print("Loading GOLD dimensions...")
    load_dim_sites(stg, gold)
    load_dim_items(stg, gold)
    load_dim_vendors(stg, gold)
    load_dim_customers(stg, gold)
    load_dim_machines(stg, gold)
    load_dim_operators(stg, gold)

    print("Loading GOLD facts...")
    load_fact_inventory(stg, gold)
    load_fact_inventory_txn(stg, gold)
    load_fact_work_orders(stg, gold)
    load_fact_throughput(stg, gold)
    load_fact_scrap(stg, gold)
    load_fact_po(stg, gold)
    load_fact_po_lines(stg, gold)
    load_fact_receipts(stg, gold)
    load_fact_customer_orders(stg, gold)
    load_fact_customer_order_lines(stg, gold)
    load_fact_shipping(stg, gold)
    load_fact_ap(stg, gold)
    load_fact_ar(stg, gold)
    load_fact_costing(stg, gold)

    conn.commit()
    conn.close()

    print("GOLD load complete.")
