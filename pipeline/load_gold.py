import sqlite3
import os
import zlib
from datetime import datetime

# ---------------------------------------------------------------------------
# GOLD LOADERS
# ---------------------------------------------------------------------------

def load_dim_sites(stg, gold):
    rows = stg.execute("""
        SELECT site_code, site_name, region, status
        FROM stg_sites_clean;
    """).fetchall()

    for r in rows:
        site_code = r["site_code"]
        site_id = abs(zlib.crc32(site_code.encode()))

        region = r["region"].strip().title() if r["region"] else None
        status = r["status"].lower()
        is_active = 1 if status == "active" else 0

        gold.execute("""
            INSERT INTO dim_sites (
                site_id, site_code, site_name, region, status,
                is_active, created_at, updated_at, source_system
            )
            VALUES (?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'), 'STAGING');
        """, (
            site_id,
            site_code,
            r["site_name"],
            region,
            status,
            is_active
        ))


def load_dim_items(stg, gold):

    rows = stg.execute("""
        SELECT item_sku, item_name, item_description,
               category, subcategory, unit_of_measure,
               standard_cost, cost_method, is_active
        FROM stg_item_clean;
    """).fetchall()

    for r in rows:
        item_sku = r["item_sku"]
        item_id = abs(zlib.crc32(item_sku.encode()))

        category = r["category"].strip().title() if r["category"] else None
        subcategory = r["subcategory"].strip().title() if r["subcategory"] else None
        uom = r["unit_of_measure"].strip().upper() if r["unit_of_measure"] else None
        cost_method = r["cost_method"].strip().upper() if r["cost_method"] else None

        is_active = 1 if r["is_active"] in ("Y", "y", 1, "true", "TRUE") else 0

        gold.execute("""
            INSERT INTO dim_item (
                item_id, item_sku, item_name, item_description,
                category, subcategory, unit_of_measure,
                standard_cost, cost_method, is_active,
                created_at, updated_at, source_system
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'), 'STAGING');
        """, (
            item_id,
            item_sku,
            r["item_name"],
            r["item_description"],
            category,
            subcategory,
            uom,
            r["standard_cost"],
            cost_method,
            is_active
        ))



def load_dim_vendors(stg, gold):
    rows = stg.execute("""
        SELECT vendor_code, vendor_name, vendor_type,
               payment_terms, country, status
        FROM stg_vendor_clean;
    """).fetchall()

    for r in rows:
        vendor_code = r["vendor_code"]
        vendor_id = abs(zlib.crc32(vendor_code.encode()))

        vendor_name = r["vendor_name"].strip() if r["vendor_name"] else None
        vendor_type = r["vendor_type"].strip().title() if r["vendor_type"] else None
        payment_terms = r["payment_terms"].strip().upper() if r["payment_terms"] else None
        country = r["country"].strip().title() if r["country"] else None

        status = r["status"].lower() if r["status"] else "inactive"
        is_active = 1 if status == "active" else 0

        gold.execute("""
            INSERT INTO dim_vendor (
                vendor_id, vendor_code, vendor_name, vendor_type,
                payment_terms, country, is_active,
                created_at, updated_at, source_system
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'), 'STAGING');
        """, (
            vendor_id,
            vendor_code,
            vendor_name,
            vendor_type,
            payment_terms,
            country,
            is_active
        ))


def load_dim_customers(stg, gold):
    rows = stg.execute("""
        SELECT customer_code, customer_name, customer_type,
               region, country, status
        FROM stg_customer_clean;
    """).fetchall()

    for r in rows:
        customer_code = r["customer_code"]
        customer_id = abs(zlib.crc32(customer_code.encode()))

        customer_name = r["customer_name"].strip() if r["customer_name"] else None
        customer_type = r["customer_type"].strip().title() if r["customer_type"] else None
        region = r["region"].strip().title() if r["region"] else None
        country = r["country"].strip().title() if r["country"] else None

        status = r["status"].lower() if r["status"] else "inactive"
        is_active = 1 if status == "active" else 0

        gold.execute("""
            INSERT INTO dim_customer (
                customer_id, customer_code, customer_name, customer_type,
                region, country, is_active,
                created_at, updated_at, source_system
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'), 'STAGING');
        """, (
            customer_id,
            customer_code,
            customer_name,
            customer_type,
            region,
            country,
            is_active
        ))


def load_dim_machines(stg, gold):
    rows = stg.execute("""
        SELECT machine_code, machine_name, machine_type,
               site_code, manufacturer, model, status
        FROM stg_machines_clean;
    """).fetchall()

    for r in rows:
        machine_code = r["machine_code"]
        machine_id = abs(zlib.crc32(machine_code.encode()))

        machine_name = r["machine_name"].strip() if r["machine_name"] else None
        machine_type = r["machine_type"].strip().title() if r["machine_type"] else None
        manufacturer = r["manufacturer"].strip().title() if r["manufacturer"] else None
        model = r["model"].strip() if r["model"] else None

        status = r["status"].lower() if r["status"] else "inactive"
        is_active = 1 if status == "active" else 0

        # site lookup
        site_id = None
        if r["site_code"]:
            row = gold.execute(
                "SELECT site_id FROM dim_sites WHERE site_code = ?;",
                (r["site_code"],)
            ).fetchone()
            if row:
                site_id = row[0]

        gold.execute("""
            INSERT INTO dim_machines (
                machine_id, machine_code, machine_name, machine_type,
                site_id, manufacturer, model, status, is_active,
                created_at, updated_at, source_system
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'), 'STAGING');
        """, (
            machine_id,
            machine_code,
            machine_name,
            machine_type,
            site_id,
            manufacturer,
            model,
            status,
            is_active
        ))

def load_dim_operators(stg, gold):
    rows = stg.execute("""
        SELECT operator_code, operator_name, operator_role,
               site_code, shift, status
        FROM stg_operators_clean;
    """).fetchall()

    for r in rows:
        operator_code = r["operator_code"]
        operator_id = abs(zlib.crc32(operator_code.encode()))

        operator_name = r["operator_name"].strip() if r["operator_name"] else None
        operator_role = r["operator_role"].strip().title() if r["operator_role"] else None
        shift = r["shift"].strip().upper() if r["shift"] else None

        status = r["status"].lower() if r["status"] else "inactive"
        is_active = 1 if status == "active" else 0

        # site lookup
        site_id = None
        if r["site_code"]:
            row = gold.execute(
                "SELECT site_id FROM dim_sites WHERE site_code = ?;",
                (r["site_code"],)
            ).fetchone()
            if row:
                site_id = row[0]

        gold.execute("""
            INSERT INTO dim_operators (
                operator_id, operator_code, operator_name, operator_role,
                site_id, shift, status, is_active,
                created_at, updated_at, source_system
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'), 'STAGING');
        """, (
            operator_id,
            operator_code,
            operator_name,
            operator_role,
            site_id,
            shift,
            status,
            is_active
        ))


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
        SELECT wo_number, site_code, item_sku,
               planned_qty, completed_qty, scrap_qty,
               start_date, end_date,
               labor_cost, material_cost
        FROM stg_work_orders_clean;
    """).fetchall()

    for r in rows:
        wo_number = r["wo_number"]
        site_code = r["site_code"]
        item_sku = r["item_sku"]

        # deterministic surrogate key
        key = f"{wo_number}|{site_code}|{item_sku}"
        work_order_id = abs(zlib.crc32(key.encode()))

        # dimension lookups
        site_id_row = gold.execute(
            "SELECT site_id FROM dim_sites WHERE site_code = ?;",
            (site_code,)
        ).fetchone()
        item_id_row = gold.execute(
            "SELECT item_id FROM dim_item WHERE item_sku = ?;",
            (item_sku,)
        ).fetchone()

        if not site_id_row or not item_id_row:
            continue

        site_id = site_id_row[0]
        item_id = item_id_row[0]

        # duration calculation
        try:
            start_dt = datetime.fromisoformat(r["start_date"])
            end_dt = datetime.fromisoformat(r["end_date"])
            duration_hours = (end_dt - start_dt).total_seconds() / 3600
        except:
            duration_hours = None

        # cost rollup
        labor_cost = r["labor_cost"] or 0
        material_cost = r["material_cost"] or 0
        total_cost = labor_cost + material_cost

        gold.execute("""
            INSERT INTO fact_work_order (
                work_order_id, wo_number, site_id, item_id,
                planned_qty, completed_qty, scrap_qty,
                start_date, end_date, duration_hours,
                labor_cost, material_cost, total_cost,
                created_at, updated_at, source_system
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'), 'STAGING');
        """, (
            work_order_id,
            wo_number,
            site_id,
            item_id,
            r["planned_qty"],
            r["completed_qty"],
            r["scrap_qty"],
            r["start_date"],
            r["end_date"],
            duration_hours,
            labor_cost,
            material_cost,
            total_cost
        ))


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
        SELECT po_number, po_line_number, vendor_code, site_code, item_sku,
               ordered_qty, received_qty, unit_price,
               order_date, promised_date, received_date
        FROM stg_po_lines_clean;
    """).fetchall()

    for r in rows:
        po_number = r["po_number"]
        po_line_number = r["po_line_number"]
        vendor_code = r["vendor_code"]
        site_code = r["site_code"]
        item_sku = r["item_sku"]

        # deterministic surrogate key
        key = f"{po_number}|{po_line_number}|{vendor_code}|{item_sku}"
        po_line_id = abs(zlib.crc32(key.encode()))

        # dimension lookups
        vendor_id_row = gold.execute(
            "SELECT vendor_id FROM dim_vendor WHERE vendor_code = ?;",
            (vendor_code,)
        ).fetchone()
        site_id_row = gold.execute(
            "SELECT site_id FROM dim_sites WHERE site_code = ?;",
            (site_code,)
        ).fetchone()
        item_id_row = gold.execute(
            "SELECT item_id FROM dim_item WHERE item_sku = ?;",
            (item_sku,)
        ).fetchone()

        if not vendor_id_row or not site_id_row or not item_id_row:
            continue

        vendor_id = vendor_id_row[0]
        site_id = site_id_row[0]
        item_id = item_id_row[0]

        # extended price
        ordered_qty = r["ordered_qty"] or 0
        unit_price = r["unit_price"] or 0
        extended_price = ordered_qty * unit_price

        # lead time calculation
        try:
            if r["received_date"]:
                order_dt = datetime.fromisoformat(r["order_date"])
                received_dt = datetime.fromisoformat(r["received_date"])
                lead_time_days = (received_dt - order_dt).days
            else:
                lead_time_days = None
        except:
            lead_time_days = None

        gold.execute("""
            INSERT INTO fact_purchase_order (
                po_line_id, po_number, po_line_number,
                vendor_id, site_id, item_id,
                ordered_qty, received_qty, unit_price, extended_price,
                order_date, promised_date, received_date, lead_time_days,
                created_at, updated_at, source_system
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'), 'STAGING');
        """, (
            po_line_id,
            po_number,
            po_line_number,
            vendor_id,
            site_id,
            item_id,
            r["ordered_qty"],
            r["received_qty"],
            unit_price,
            extended_price,
            r["order_date"],
            r["promised_date"],
            r["received_date"],
            lead_time_days
        ))


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
        SELECT shipment_number, shipment_line_number, customer_code,
               site_code, item_sku, shipped_qty, invoiced_qty,
               revenue, discount, shipment_date, promised_date, delivered_date
        FROM stg_shipments_clean;
    """).fetchall()

    for r in rows:
        shipment_number = r["shipment_number"]
        shipment_line_number = r["shipment_line_number"]
        customer_code = r["customer_code"]
        site_code = r["site_code"]
        item_sku = r["item_sku"]

        # deterministic surrogate key
        key = f"{shipment_number}|{shipment_line_number}|{customer_code}|{item_sku}"
        shipment_line_id = abs(zlib.crc32(key.encode()))

        # dimension lookups
        customer_id_row = gold.execute(
            "SELECT customer_id FROM dim_customer WHERE customer_code = ?;",
            (customer_code,)
        ).fetchone()
        site_id_row = gold.execute(
            "SELECT site_id FROM dim_sites WHERE site_code = ?;",
            (site_code,)
        ).fetchone()
        item_id_row = gold.execute(
            "SELECT item_id FROM dim_item WHERE item_sku = ?;",
            (item_sku,)
        ).fetchone()

        if not customer_id_row or not site_id_row or not item_id_row:
            continue

        customer_id = customer_id_row[0]
        site_id = site_id_row[0]
        item_id = item_id_row[0]

        # delivery days calculation
        try:
            if r["delivered_date"]:
                ship_dt = datetime.fromisoformat(r["shipment_date"])
                delivered_dt = datetime.fromisoformat(r["delivered_date"])
                delivery_days = (delivered_dt - ship_dt).days
            else:
                delivery_days = None
        except:
            delivery_days = None

        gold.execute("""
            INSERT INTO fact_shipment (
                shipment_line_id, shipment_number, shipment_line_number,
                customer_id, site_id, item_id,
                shipped_qty, invoiced_qty, revenue, discount,
                shipment_date, promised_date, delivered_date, delivery_days,
                created_at, updated_at, source_system
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'), 'STAGING');
        """, (
            shipment_line_id,
            shipment_number,
            shipment_line_number,
            customer_id,
            site_id,
            item_id,
            r["shipped_qty"],
            r["invoiced_qty"],
            r["revenue"],
            r["discount"],
            r["shipment_date"],
            r["promised_date"],
            r["delivered_date"],
            delivery_days
        ))


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

def load_fact_inventory_snapshot(stg, gold):
    rows = stg.execute("""
        SELECT snapshot_date, site_code, item_sku,
               quantity_on_hand, quantity_reserved, quantity_available
        FROM stg_inventory_clean;
    """).fetchall()

    for r in rows:
        snapshot_date = r["snapshot_date"]
        site_code = r["site_code"]
        item_sku = r["item_sku"]

        # deterministic surrogate key
        snapshot_key = f"{snapshot_date}|{site_code}|{item_sku}"
        snapshot_id = abs(zlib.crc32(snapshot_key.encode()))

        # dimension lookups
        site_id_row = gold.execute(
            "SELECT site_id FROM dim_sites WHERE site_code = ?;",
            (site_code,)
        ).fetchone()
        item_id_row = gold.execute(
            "SELECT item_id FROM dim_item WHERE item_sku = ?;",
            (item_sku,)
        ).fetchone()

        if not site_id_row or not item_id_row:
            continue  # skip bad rows

        site_id = site_id_row[0]
        item_id = item_id_row[0]

        # inventory valuation
        standard_cost_row = gold.execute(
            "SELECT standard_cost FROM dim_item WHERE item_id = ?;",
            (item_id,)
        ).fetchone()
        standard_cost = standard_cost_row[0] if standard_cost_row else 0

        inventory_value = (r["quantity_on_hand"] or 0) * (standard_cost or 0)

        gold.execute("""
            INSERT INTO fact_inventory_snapshot (
                snapshot_id, snapshot_date, site_id, item_id,
                quantity_on_hand, quantity_reserved, quantity_available,
                inventory_value, created_at, updated_at, source_system
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'), 'STAGING');
        """, (
            snapshot_id,
            snapshot_date,
            site_id,
            item_id,
            r["quantity_on_hand"],
            r["quantity_reserved"],
            r["quantity_available"],
            inventory_value
        ))

def load_fact_sales(stg, gold):
    rows = stg.execute("""
        SELECT invoice_number, invoice_line_number, customer_code,
               site_code, item_sku, sold_qty, unit_price, discount,
               invoice_date
        FROM stg_sales_clean;
    """).fetchall()

    for r in rows:
        invoice_number = r["invoice_number"]
        invoice_line_number = r["invoice_line_number"]
        customer_code = r["customer_code"]
        site_code = r["site_code"]
        item_sku = r["item_sku"]

        # deterministic surrogate key
        key = f"{invoice_number}|{invoice_line_number}|{customer_code}|{item_sku}"
        sales_line_id = abs(zlib.crc32(key.encode()))

        # dimension lookups
        customer_id_row = gold.execute(
            "SELECT customer_id FROM dim_customer WHERE customer_code = ?;",
            (customer_code,)
        ).fetchone()
        site_id_row = gold.execute(
            "SELECT site_id FROM dim_sites WHERE site_code = ?;",
            (site_code,)
        ).fetchone()
        item_id_row = gold.execute(
            "SELECT item_id FROM dim_item WHERE item_sku = ?;",
            (item_sku,)
        ).fetchone()

        if not customer_id_row or not site_id_row or not item_id_row:
            continue

        customer_id = customer_id_row[0]
        site_id = site_id_row[0]
        item_id = item_id_row[0]

        # revenue calculations
        sold_qty = r["sold_qty"] or 0
        unit_price = r["unit_price"] or 0
        discount = r["discount"] or 0

        extended_price = sold_qty * unit_price
        net_revenue = extended_price - discount

        gold.execute("""
            INSERT INTO fact_sales (
                sales_line_id, invoice_number, invoice_line_number,
                customer_id, site_id, item_id,
                sold_qty, unit_price, extended_price, discount, net_revenue,
                invoice_date, created_at, updated_at, source_system
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'), 'STAGING');
        """, (
            sales_line_id,
            invoice_number,
            invoice_line_number,
            customer_id,
            site_id,
            item_id,
            sold_qty,
            unit_price,
            extended_price,
            discount,
            net_revenue,
            r["invoice_date"]
        ))

def load_fact_financials(stg, gold):
    rows = stg.execute("""
        SELECT gl_account_code, gl_account_name, gl_category, gl_subcategory,
               fiscal_year, fiscal_period, posting_date,
               site_code, item_sku, customer_code, vendor_code,
               debit, credit
        FROM stg_financials_clean;
    """).fetchall()

    for r in rows:
        gl_account_code = r["gl_account_code"]
        posting_date = r["posting_date"]
        debit = r["debit"] or 0
        credit = r["credit"] or 0

        # deterministic surrogate key
        key = f"{gl_account_code}|{posting_date}|{debit}|{credit}"
        gl_line_id = abs(zlib.crc32(key.encode()))

        # dimension lookups (optional)
        site_id = None
        item_id = None
        customer_id = None
        vendor_id = None

        if r["site_code"]:
            row = gold.execute("SELECT site_id FROM dim_sites WHERE site_code = ?;", (r["site_code"],)).fetchone()
            if row: site_id = row[0]

        if r["item_sku"]:
            row = gold.execute("SELECT item_id FROM dim_item WHERE item_sku = ?;", (r["item_sku"],)).fetchone()
            if row: item_id = row[0]

        if r["customer_code"]:
            row = gold.execute("SELECT customer_id FROM dim_customer WHERE customer_code = ?;", (r["customer_code"],)).fetchone()
            if row: customer_id = row[0]

        if r["vendor_code"]:
            row = gold.execute("SELECT vendor_id FROM dim_vendor WHERE vendor_code = ?;", (r["vendor_code"],)).fetchone()
            if row: vendor_id = row[0]

        # financial amount
        amount = debit - credit

        gold.execute("""
            INSERT INTO fact_financials (
                gl_line_id, gl_account_code, gl_account_name, gl_category, gl_subcategory,
                fiscal_year, fiscal_period, posting_date,
                site_id, item_id, customer_id, vendor_id,
                debit, credit, amount,
                created_at, updated_at, source_system
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'), 'STAGING');
        """, (
            gl_line_id,
            gl_account_code,
            r["gl_account_name"],
            r["gl_category"],
            r["gl_subcategory"],
            r["fiscal_year"],
            r["fiscal_period"],
            posting_date,
            site_id,
            item_id,
            customer_id,
            vendor_id,
            debit,
            credit,
            amount
        ))

def load_fact_machine_usage(stg, gold):
    rows = stg.execute("""
        SELECT machine_code, operator_code, site_code,
               start_time, end_time,
               runtime_minutes, downtime_minutes,
               reason_code, work_order_number
        FROM stg_machine_usage_clean;
    """).fetchall()

    for r in rows:
        machine_code = r["machine_code"]
        operator_code = r["operator_code"]
        site_code = r["site_code"]
        start_time = r["start_time"]
        end_time = r["end_time"]

        # deterministic surrogate key
        key = f"{machine_code}|{operator_code}|{start_time}|{end_time}"
        usage_id = abs(zlib.crc32(key.encode()))

        # dimension lookups
        machine_id_row = gold.execute(
            "SELECT machine_id FROM dim_machines WHERE machine_code = ?;",
            (machine_code,)
        ).fetchone()

        site_id_row = gold.execute(
            "SELECT site_id FROM dim_sites WHERE site_code = ?;",
            (site_code,)
        ).fetchone()

        operator_id_row = None
        if operator_code:
            operator_id_row = gold.execute(
                "SELECT operator_id FROM dim_operators WHERE operator_code = ?;",
                (operator_code,)
            ).fetchone()

        work_order_id_row = None
        if r["work_order_number"]:
            work_order_id_row = gold.execute(
                "SELECT work_order_id FROM fact_work_order WHERE wo_number = ?;",
                (r["work_order_number"],)
            ).fetchone()

        if not machine_id_row or not site_id_row:
            continue

        machine_id = machine_id_row[0]
        site_id = site_id_row[0]
        operator_id = operator_id_row[0] if operator_id_row else None
        work_order_id = work_order_id_row[0] if work_order_id_row else None

        # total minutes
        runtime = r["runtime_minutes"] or 0
        downtime = r["downtime_minutes"] or 0
        total_minutes = runtime + downtime

        gold.execute("""
            INSERT INTO fact_machine_usage (
                usage_id, machine_id, operator_id, site_id, work_order_id,
                start_time, end_time, runtime_minutes, downtime_minutes,
                total_minutes, reason_code,
                created_at, updated_at, source_system
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'), 'STAGING');
        """, (
            usage_id,
            machine_id,
            operator_id,
            site_id,
            work_order_id,
            start_time,
            end_time,
            runtime,
            downtime,
            total_minutes,
            r["reason_code"]
        ))

def load_fact_operator_efficency(stg, gold):
    rows = stg.execute("""
        SELECT operator_code, machine_code, site_code, shift,
               start_time, end_time,
               runtime_minutes, downtime_minutes,
               work_order_number
        FROM stg_operator_efficiency_clean;
    """).fetchall()

    for r in rows:
        operator_code = r["operator_code"]
        machine_code = r["machine_code"]
        site_code = r["site_code"]
        start_time = r["start_time"]
        end_time = r["end_time"]

        # deterministic surrogate key
        key = f"{operator_code}|{machine_code}|{start_time}|{end_time}"
        efficiency_id = abs(zlib.crc32(key.encode()))

        # dimension lookups
        operator_id_row = gold.execute(
            "SELECT operator_id FROM dim_operators WHERE operator_code = ?;",
            (operator_code,)
        ).fetchone()

        machine_id_row = None
        if machine_code:
            machine_id_row = gold.execute(
                "SELECT machine_id FROM dim_machines WHERE machine_code = ?;",
                (machine_code,)
            ).fetchone()

        site_id_row = gold.execute(
            "SELECT site_id FROM dim_sites WHERE site_code = ?;",
            (site_code,)
        ).fetchone()

        work_order_id_row = None
        if r["work_order_number"]:
            work_order_id_row = gold.execute(
                "SELECT work_order_id FROM fact_work_order WHERE wo_number = ?;",
                (r["work_order_number"],)
            ).fetchone()

        if not operator_id_row or not site_id_row:
            continue

        operator_id = operator_id_row[0]
        machine_id = machine_id_row[0] if machine_id_row else None
        site_id = site_id_row[0]
        work_order_id = work_order_id_row[0] if work_order_id_row else None

        # efficiency calculations
        runtime = r["runtime_minutes"] or 0
        downtime = r["downtime_minutes"] or 0
        total_minutes = runtime + downtime

        utilization = None
        if total_minutes > 0:
            utilization = runtime / total_minutes

        gold.execute("""
            INSERT INTO fact_operator_efficiency (
                efficiency_id, operator_id, machine_id, site_id, work_order_id,
                start_time, end_time, runtime_minutes, downtime_minutes,
                total_minutes, utilization, shift,
                created_at, updated_at, source_system
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'), 'STAGING');
        """, (
            efficiency_id,
            operator_id,
            machine_id,
            site_id,
            work_order_id,
            start_time,
            end_time,
            runtime,
            downtime,
            total_minutes,
            utilization,
            r["shift"]
        ))

def load_fact_machine_downtime(stg, gold):
    rows = stg.execute("""
        SELECT machine_code, operator_code, site_code,
               start_time, end_time, downtime_minutes,
               reason_code, reason_category, work_order_number
        FROM stg_machine_downtime_clean;
    """).fetchall()

    for r in rows:
        machine_code = r["machine_code"]
        operator_code = r["operator_code"]
        site_code = r["site_code"]
        start_time = r["start_time"]
        end_time = r["end_time"]
        reason_code = r["reason_code"]

        # deterministic surrogate key
        key = f"{machine_code}|{start_time}|{end_time}|{reason_code}"
        downtime_id = abs(zlib.crc32(key.encode()))

        # dimension lookups
        machine_id_row = gold.execute(
            "SELECT machine_id FROM dim_machines WHERE machine_code = ?;",
            (machine_code,)
        ).fetchone()

        site_id_row = gold.execute(
            "SELECT site_id FROM dim_sites WHERE site_code = ?;",
            (site_code,)
        ).fetchone()

        operator_id_row = None
        if operator_code:
            operator_id_row = gold.execute(
                "SELECT operator_id FROM dim_operators WHERE operator_code = ?;",
                (operator_code,)
            ).fetchone()

        work_order_id_row = None
        if r["work_order_number"]:
            work_order_id_row = gold.execute(
                "SELECT work_order_id FROM fact_work_order WHERE wo_number = ?;",
                (r["work_order_number"],)
            ).fetchone()

        if not machine_id_row or not site_id_row:
            continue

        machine_id = machine_id_row[0]
        site_id = site_id_row[0]
        operator_id = operator_id_row[0] if operator_id_row else None
        work_order_id = work_order_id_row[0] if work_order_id_row else None

        downtime_minutes = r["downtime_minutes"] or 0

        gold.execute("""
            INSERT INTO fact_machine_downtime (
                downtime_id, machine_id, operator_id, site_id, work_order_id,
                start_time, end_time, downtime_minutes,
                reason_code, reason_category,
                created_at, updated_at, source_system
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'), 'STAGING');
        """, (
            downtime_id,
            machine_id,
            operator_id,
            site_id,
            work_order_id,
            start_time,
            end_time,
            downtime_minutes,
            reason_code,
            r["reason_category"]
        ))

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
    load_fact_sales(stg,gold)
    load_fact_financials(stg, gold)
    load_fact_machine_usage(stg, gold)
    load_fact_operator_efficency(stg, gold)
    load_fact_machine_downtime(stg, gold)

    conn.commit()
    conn.close()

    print("GOLD load complete.")
