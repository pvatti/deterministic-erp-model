def transform_po_lines(raw, stg, ex):
    """
    RAW: po_lines_raw
        po_line_id, po_id, item_id, ordered_quantity, uom, notes

    STAGING: stg_po_lines_clean
        po_line_key, po_line_id, po_key, item_key,
        ordered_quantity, uom, notes
    """

    po_line_id, po_id, item_id, ordered_quantity, uom, notes = raw

    # Lookup po_key
    po_row = stg.execute(
        "SELECT po_key FROM stg_po_clean WHERE po_id = ?;",
        (po_id,)
    ).fetchone()
    if po_row is None:
        ex.execute("""
            INSERT INTO stg_exceptions (
                source_table, source_record_id, exception_type, severity,
                description, timestamp, rule_name
            )
            VALUES ('po_lines_raw', ?, 'Missing PO', 'high',
                    'po_id not found in stg_po_clean', datetime('now'),
                    'transform_po_lines');
        """, (po_line_id,))
        return
    po_key = po_row[0]

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
            VALUES ('po_lines_raw', ?, 'Missing item', 'high',
                    'item_id not found in stg_items_clean', datetime('now'),
                    'transform_po_lines');
        """, (po_line_id,))
        return
    item_key = item_row[0]

    # Normalize
    uom = uom.strip()
    notes = notes.strip() if notes else None

    stg.execute("""
        INSERT INTO stg_po_lines_clean (
            po_line_key,
            po_line_id,
            po_key,
            item_key,
            ordered_quantity,
            uom,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (
        po_line_id,
        po_line_id,
        po_key,
        item_key,
        ordered_quantity,
        uom,
        notes
    ))
