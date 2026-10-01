def transform_work_orders(raw, stg, ex):
    """
    RAW: work_orders_raw
        work_order_id, site_id, item_id, planned_quantity,
        scheduled_start, scheduled_end, status, created_by

    STAGING: stg_work_orders_clean
        wo_key, work_order_id, site_key, item_key,
        planned_quantity, scheduled_start, scheduled_end,
        status, created_by
    """

    (work_order_id, site_id, item_id, planned_quantity,
     scheduled_start, scheduled_end, status, created_by) = raw

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
            VALUES ('work_orders_raw', ?, 'Missing site', 'high',
                    'site_id not found in stg_sites_clean', datetime('now'),
                    'transform_work_orders');
        """, (work_order_id,))
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
            VALUES ('work_orders_raw', ?, 'Missing item', 'high',
                    'item_id not found in stg_items_clean', datetime('now'),
                    'transform_work_orders');
        """, (work_order_id,))
        return
    item_key = item_row[0]

    # Normalize
    status = status.strip() if status else None
    created_by = created_by.strip() if created_by else None

    stg.execute("""
        INSERT INTO stg_work_orders_clean (
            wo_key,
            work_order_id,
            site_key,
            item_key,
            planned_quantity,
            scheduled_start,
            scheduled_end,
            status,
            created_by
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        work_order_id,
        work_order_id,
        site_key,
        item_key,
        planned_quantity,
        scheduled_start,
        scheduled_end,
        status,
        created_by
    ))
