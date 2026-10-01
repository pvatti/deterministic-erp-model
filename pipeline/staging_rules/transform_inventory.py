def transform_inventory(raw, stg, ex):
    """
    RAW: inventory_raw
        inventory_id, site_id, item_id, quantity_on_hand,
        location_code, last_updated_at, last_updated_by, notes

    STAGING: stg_inventory_clean
        inventory_key, inventory_id, site_key, item_key,
        quantity_on_hand, location_code, last_updated_at, last_updated_by
    """

    (inventory_id, site_id, item_id, quantity_on_hand,
     location_code, last_updated_at, last_updated_by, notes) = raw

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
            VALUES ('inventory_raw', ?, 'Missing site', 'high',
                    'site_id not found in stg_sites_clean', datetime('now'),
                    'transform_inventory');
        """, (inventory_id,))
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
            VALUES ('inventory_raw', ?, 'Missing item', 'high',
                    'item_id not found in stg_items_clean', datetime('now'),
                    'transform_inventory');
        """, (inventory_id,))
        return
    item_key = item_row[0]

    # Normalize
    location_code = location_code.strip() if location_code else None
    last_updated_by = last_updated_by.strip() if last_updated_by else None

    stg.execute("""
        INSERT INTO stg_inventory_clean (
            inventory_key,
            inventory_id,
            site_key,
            item_key,
            quantity_on_hand,
            location_code,
            last_updated_at,
            last_updated_by
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        inventory_id,
        inventory_id,
        site_key,
        item_key,
        quantity_on_hand,
        location_code,
        last_updated_at,
        last_updated_by
    ))
