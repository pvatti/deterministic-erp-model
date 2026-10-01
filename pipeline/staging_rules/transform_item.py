def transform_items(raw, stg, ex):
    """
    RAW: items
        item_id, item_sku, item_name, item_type, uom, status

    STAGING: stg_items_clean
        item_key, item_id, item_sku, item_name, item_type, uom, status
    """
    item_id, item_sku, item_name, item_type, uom, status = raw

    # Validate item_type
    if item_type not in ("FG", "WIP", "RM"):
        ex.execute("""
            INSERT INTO stg_exceptions (
                source_table, source_record_id, exception_type,
                severity, description, timestamp, rule_name
            )
            VALUES ('items', ?, 'Invalid item_type', 'high',
                    'Item type must be FG, WIP, or RM', datetime('now'), 'transform_items');
        """, (item_id,))
        return

    # Validate status
    if status not in ("active", "inactive"):
        ex.execute("""
            INSERT INTO stg_exceptions (
                source_table, source_record_id, exception_type,
                severity, description, timestamp, rule_name
            )
            VALUES ('items', ?, 'Invalid status', 'high',
                    'Status must be active or inactive', datetime('now'), 'transform_items');
        """, (item_id,))
        return

    # Normalize
    item_sku = item_sku.strip()
    item_name = item_name.strip()
    item_type = item_type.strip()
    uom = uom.strip()

    stg.execute("""
        INSERT INTO stg_items_clean (
            item_key,
            item_id,
            item_sku,
            item_name,
            item_type,
            uom,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (
        item_id,
        item_id,
        item_sku,
        item_name,
        item_type,
        uom,
        status
    ))
