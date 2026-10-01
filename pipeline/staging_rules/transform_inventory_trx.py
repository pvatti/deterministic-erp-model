def transform_inventory_transactions(raw, stg, ex):
    """
    RAW: inventory_transactions_raw
        txn_id, site_id, item_id, txn_type, quantity,
        timestamp, reference_id, notes

    STAGING: stg_inventory_txn_clean
        txn_key, txn_id, site_key, item_key, txn_type,
        quantity, timestamp, reference_id, notes
    """

    (txn_id, site_id, item_id, txn_type, quantity,
     timestamp, reference_id, notes) = raw

    # Lookup site_key
    site_row = stg.execute(
        "SELECT site_key FROM stg_sites_clean WHERE site_id = ?;",
        (site_id,)
    ).fetchone()
    if site_row is None:
        ex.execute("""
            INSERT INTO stg_exceptions (
                source_table, source_record_id, exception_type, severity,
                description, timestamp, rule_name
            )
            VALUES ('inventory_transactions_raw', ?, 'Missing site', 'high',
                    'site_id not found in stg_sites_clean', datetime('now'),
                    'transform_inventory_transactions');
        """, (txn_id,))
        return
    site_key = site_row[0]

    # Lookup item_key
    item_row = stg.execute(
        "SELECT item_key FROM stg_items_clean WHERE item_id = ?;",
        (item_id,)
    ).fetchone()
    if item_row is None:
        ex.execute("""
            INSERT INTO stg_exceptions (
                source_table, source_record_id, exception_type, severity,
                description, timestamp, rule_name
            )
            VALUES ('inventory_transactions_raw', ?, 'Missing item', 'high',
                    'item_id not found in stg_items_clean', datetime('now'),
                    'transform_inventory_transactions');
        """, (txn_id,))
        return
    item_key = item_row[0]

    # Normalize
    txn_type = txn_type.strip()
    notes = notes.strip() if notes else None

    stg.execute("""
        INSERT INTO stg_inventory_txn_clean (
            txn_key,
            txn_id,
            site_key,
            item_key,
            txn_type,
            quantity,
            timestamp,
            reference_id,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        txn_id,
        txn_id,
        site_key,
        item_key,
        txn_type,
        quantity,
        timestamp,
        reference_id,
        notes
    ))
