def transform_ap(raw, stg, ex):
    """
    RAW: ap_raw
        ap_id, vendor_id, amount, due_date, status

    STAGING: stg_ap_clean
        ap_key, ap_id, vendor_key, amount, due_date, status
    """

    ap_id, vendor_id, amount, due_date, status = raw

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
            VALUES ('ap_raw', ?, 'Missing vendor', 'high',
                    'vendor_id not found in stg_vendors_clean', datetime('now'),
                    'transform_ap');
        """, (ap_id,))
        return
    vendor_key = vendor_row[0]

    # Normalize
    status = status.strip() if status else None

    stg.execute("""
        INSERT INTO stg_ap_clean (
            ap_key,
            ap_id,
            vendor_key,
            amount,
            due_date,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?);
    """, (
        ap_id,
        ap_id,
        vendor_key,
        amount,
        due_date,
        status
    ))
