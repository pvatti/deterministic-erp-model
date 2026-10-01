def transform_receipts(raw, stg, ex):
    """
    RAW: receipts_raw
        receipt_id, po_line_id, received_quantity, timestamp, received_by

    STAGING: stg_receipts_clean
        receipt_key, receipt_id, po_line_key,
        received_quantity, timestamp, received_by
    """

    receipt_id, po_line_id, received_quantity, timestamp, received_by = raw

    # Lookup po_line_key
    po_line_row = stg.execute(
        "SELECT po_line_key FROM stg_po_lines_clean WHERE po_line_id = ?;",
        (po_line_id,)
    ).fetchone()
    if po_line_row is None:
        ex.execute("""
            INSERT INTO stg_exceptions (
                source_table, source_record_id, exception_type, severity,
                description, timestamp, rule_name
            )
            VALUES ('receipts_raw', ?, 'Missing PO line', 'high',
                    'po_line_id not found in stg_po_lines_clean', datetime('now'),
                    'transform_receipts');
        """, (receipt_id,))
        return
    po_line_key = po_line_row[0]

    # Normalize
    received_by = received_by.strip() if received_by else None

    stg.execute("""
        INSERT INTO stg_receipts_clean (
            receipt_key,
            receipt_id,
            po_line_key,
            received_quantity,
            timestamp,
            received_by
        )
        VALUES (?, ?, ?, ?, ?, ?);
    """, (
        receipt_id,
        receipt_id,
        po_line_key,
        received_quantity,
        timestamp,
        received_by
    ))
