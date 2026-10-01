def transform_scrap(raw, stg, ex):
    """
    RAW: scrap_raw
        scrap_id, site_id, item_id, quantity,
        reason, timestamp, operator_id

    STAGING: stg_scrap_clean
        scrap_key, scrap_id, site_key, item_key,
        quantity, reason, timestamp, operator_key
    """

    (scrap_id, site_id, item_id, quantity,
     reason, timestamp, operator_id) = raw

    # Lookup site_key
    site_key = stg.execute(
        "SELECT site_key FROM stg_sites_clean WHERE site_id = ?;",
        (site_id,)
    ).fetchone()
    if site_key is None:
        ex.execute("""
            INSERT INTO stg_exceptions (
                source_table, source_record_id, exception_type, severity,
                description, timestamp, rule_name
            )
            VALUES ('scrap_raw', ?, 'Missing site', 'high',
                    'site_id not found in stg_sites_clean', datetime('now'),
                    'transform_scrap');
        """, (scrap_id,))
        return
    site_key = site_key[0]

    # Lookup item_key
    item_key = stg.execute(
        "SELECT item_key FROM stg_items_clean WHERE item_id = ?;",
        (item_id,)
    ).fetchone()
    if item_key is None:
        ex.execute("""
            INSERT INTO stg_exceptions (
                source_table, source_record_id, exception_type, severity,
                description, timestamp, rule_name
            )
            VALUES ('scrap_raw', ?, 'Missing item', 'high',
                    'item_id not found in stg_items_clean', datetime('now'),
                    'transform_scrap');
        """, (scrap_id,))
        return
    item_key = item_key[0]

    # Lookup operator_key (optional)
    operator_key = None
    if operator_id:
        op_row = stg.execute(
            "SELECT operator_key FROM stg_operators_clean WHERE operator_id = ?;",
            (operator_id,)
        ).fetchone()
        operator_key = op_row[0] if op_row else None

    # Normalize
    reason = reason.strip() if reason else None

    stg.execute("""
        INSERT INTO stg_scrap_clean (
            scrap_key,
            scrap_id,
            site_key,
            item_key,
            quantity,
            reason,
            timestamp,
            operator_key
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        scrap_id,
        scrap_id,
        site_key,
        item_key,
        quantity,
        reason,
        timestamp,
        operator_key
    ))
