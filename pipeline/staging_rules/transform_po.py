def transform_po(raw, stg, ex):
    """
    RAW: purchase_orders_raw
        po_id, vendor_id, po_date, status, created_by

    STAGING: stg_po_clean
        po_key, po_id, vendor_key, po_date, status, created_by
    """

    po_id, vendor_id, po_date, status, created_by = raw

    # Lookup vendor_key
    vendor_row = stg.execute(
        "SELECT vendor_key FROM stg_vendors_clean WHERE vendor_id = ?;",
        (vendor_id,)
    ).fetchone()
    if vendor_row is None:
        ex.execute("""
            INSERT INTO stg_exceptions (
                source_table, source_record_id, exception_type, severity,
                description, timestamp, rule_name
            )
            VALUES ('purchase_orders_raw', ?, 'Missing vendor', 'high',
                    'vendor_id not found in stg_vendors_clean', datetime('now'),
                    'transform_po');
        """, (po_id,))
        return
    vendor_key = vendor_row[0]

    # Normalize
    status = status.strip() if status else None
    created_by = created_by.strip() if created_by else None

    stg.execute("""
        INSERT INTO stg_po_clean (
            po_key,
            po_id,
            vendor_key,
            po_date,
            status,
            created_by
        )
        VALUES (?, ?, ?, ?, ?, ?);
    """, (
        po_id,
        po_id,
        vendor_key,
        po_date,
        status,
        created_by
    ))
