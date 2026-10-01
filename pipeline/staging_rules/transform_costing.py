def transform_costing(raw, stg, ex):
    """
    RAW: costing_raw
        cost_id, item_id, site_id, standard_cost,
        last_updated_at, updated_by

    STAGING: stg_costing_clean
        cost_key, cost_id, item_key, site_key,
        standard_cost, last_updated_at, updated_by
    """

    cost_id, item_id, site_id, standard_cost, last_updated_at, updated_by = raw

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
            VALUES ('costing_raw', ?, 'Missing item', 'high',
                    'item_id not found in stg_items_clean', datetime('now'),
                    'transform_costing');
        """, (cost_id,))
        return
    item_key = item_row[0]

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
            VALUES ('costing_raw', ?, 'Missing site', 'high',
                    'site_id not found in stg_sites_clean', datetime('now'),
                    'transform_costing');
        """, (cost_id,))
        return
    site_key = site_row[0]

    # Normalize
    updated_by = updated_by.strip() if updated_by else None

    stg.execute("""
        INSERT INTO stg_costing_clean (
            cost_key,
            cost_id,
            item_key,
            site_key,
            standard_cost,
            last_updated_at,
            updated_by
        )
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (
        cost_id,
        cost_id,
        item_key,
        site_key,
        standard_cost,
        last_updated_at,
        updated_by
    ))
