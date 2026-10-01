import sqlite3
from staging_rules.transform_site import transform_sites
from staging_rules.transform_item import transform_items
from staging_rules.transform_vendor import transform_vendors
from staging_rules.transform_customer import transform_customers
from staging_rules.transform_machine import transform_machines
from staging_rules.transform_operator import transform_operators

from staging_rules.transform_inventory import transform_inventory
from staging_rules.transform_inventory_trx import transform_inventory_transactions
from staging_rules.transform_work_order import transform_work_orders
from staging_rules.transform_throughput import transform_throughput
from staging_rules.transform_scrap import transform_scrap

from staging_rules.transform_po import transform_po
from staging_rules.transform_po_lines import transform_po_lines
from staging_rules.transform_recepits import transform_receipts

from staging_rules.transform_customer_order import transform_customer_orders
from staging_rules.transform_customer_order_line import transform_customer_order_lines
from staging_rules.transform_shipment import transform_shipping

from staging_rules.transform_ap import transform_ap
from staging_rules.transform_ar import transform_ar
from staging_rules.transform_costing import transform_costing


# ---------------------------------------------------------------------------
# TRANSFORM MAP
# ---------------------------------------------------------------------------

TRANSFORM_MAP = {
    # MASTER DATA
    "sites": transform_sites,
    "items": transform_items,
    "vendors": transform_vendors,
    "customers": transform_customers,
    "machines": transform_machines,
    "operators": transform_operators,

    # INVENTORY
    "inventory_raw": transform_inventory,
    "inventory_transactions_raw": transform_inventory_transactions,

    # PRODUCTION
    "work_orders_raw": transform_work_orders,
    "throughput_raw": transform_throughput,
    "scrap_raw": transform_scrap,

    # PROCUREMENT
    "purchase_orders_raw": transform_po,
    "po_lines_raw": transform_po_lines,
    "receipts_raw": transform_receipts,

    # SALES
    "customer_orders_raw": transform_customer_orders,
    "customer_order_lines_raw": transform_customer_order_lines,
    "shipping_raw": transform_shipping,

    # FINANCE
    "ap_raw": transform_ap,
    "ar_raw": transform_ar,
    "costing_raw": transform_costing
}


# ---------------------------------------------------------------------------
# LOAD STAGING
# ---------------------------------------------------------------------------

def load_staging():
    """
    Loads RAW → STAGING using deterministic transform rules.
    Applies:
        - validation
        - normalization
        - surrogate-key resolution
        - exception logging
    """

    # Connect to staging DB
    conn = sqlite3.connect("data/staging.db")
    stg = conn.cursor()

    # Attach RAW DB
    conn.execute("ATTACH DATABASE 'data/raw.db' AS raw;")

    # Exception logging cursor
    ex = conn.cursor()

    # Iterate through each RAW table in deterministic order
    for raw_table, transform_func in TRANSFORM_MAP.items():

        print(f"Loading {raw_table}...")

        # Pull all rows from RAW table
        raw_rows = stg.execute(f"SELECT * FROM raw.{raw_table};").fetchall()

        # Apply transform rule to each row
        for raw_row in raw_rows:
            try:
                transform_func(raw_row, stg, ex)
            except Exception as e:
                ex.execute("""
                    INSERT INTO stg_exceptions (
                        source_table, source_record_id, exception_type,
                        severity, description, timestamp, rule_name
                    )
                    VALUES (?, ?, 'Transform error', 'high', ?, datetime('now'), ?);
                """, (
                    raw_table,
                    raw_row[0],
                    str(e),
                    transform_func.__name__
                ))

        conn.commit()

    print("STAGING load complete.")
    conn.close()


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    load_staging()
