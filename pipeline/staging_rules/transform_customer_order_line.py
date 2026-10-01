def transform_customer_order_lines(raw, stg, ex):
    """
    RAW: customer_order_lines_raw
        order_line_id, order_id, item_id,
        ordered_quantity, uom, notes

    STAGING: stg_customer_order_lines_clean
        order_line_key, order_line_id, order_key,
        item_key, ordered_quantity, uom, notes
    """

    order_line_id, order_id, item_id, ordered_quantity, uom, notes = raw

    # Lookup order_key
    order_row = stg.execute(
        "SELECT order_key FROM stg_customer_orders_clean WHERE order_id = ?;",
        (order_id,)
    ).fetchone()
    if order_row is None:
        ex.execute("""
            INSERT INTO stg_exceptions (
                source_table, source_record_id, exception_type, severity,
                description, timestamp, rule_name
            )
            VALUES ('customer_order_lines_raw', ?, 'Missing order', 'high',
                    'order_id not found in stg_customer_orders_clean', datetime('now'),
                    'transform_customer_order_lines');
        """, (order_line_id,))
        return
    order_key = order_row[0]

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
            VALUES ('customer_order_lines_raw', ?, 'Missing item', 'high',
                    'item_id not found in stg_items_clean', datetime('now'),
                    'transform_customer_order_lines');
        """, (order_line_id,))
        return
    item_key = item_row[0]

    # Normalize
    uom = uom.strip()
    notes = notes.strip() if notes else None

    stg.execute("""
        INSERT INTO stg_customer_order_lines_clean (
            order_line_key,
            order_line_id,
            order_key,
            item_key,
            ordered_quantity,
            uom,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (
        order_line_id,
        order_line_id,
        order_key,
        item_key,
        ordered_quantity,
        uom,
        notes
    ))
