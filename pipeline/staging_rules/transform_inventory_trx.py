def transform_inventory_txn(raw, stg, ex, site_map, item_map):
    txn_id, site_id, item_id, txn_type, qty, ts, ref, notes = raw

    if site_id not in site_map:
        ex.execute(...); return
    if item_id not in item_map:
        ex.execute(...); return

    # Business rule: txn_type must be valid
    if txn_type not in ("RECEIPT", "ISSUE", "ADJUSTMENT"):
        ex.execute(...); return

    ts = ts.replace(" ", "T")

    stg.execute("""
        INSERT INTO stg_inventory_txn_clean (
            txn_key, txn_id, site_key, item_key, txn_type,
            quantity, timestamp, reference_id, notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (txn_id, txn_id, site_map[site_id], item_map[item_id], txn_type, qty, ts, ref, notes))
