def transform_vendors(raw, stg, ex):
    """
    RAW: vendors
        vendor_id, vendor_code, vendor_name, status

    STAGING: stg_vendors_clean
        vendor_key, vendor_id, vendor_code, vendor_name, status
    """
    vendor_id, vendor_code, vendor_name, status = raw

    if status not in ("active", "inactive"):
        ex.execute("""
            INSERT INTO stg_exceptions (
                source_table, source_record_id, exception_type,
                severity, description, timestamp, rule_name
            )
            VALUES ('vendors', ?, 'Invalid status', 'high',
                    'Status must be active or inactive', datetime('now'), 'transform_vendors');
        """, (vendor_id,))
        return

    vendor_code = vendor_code.strip()
    vendor_name = vendor_name.strip()

    stg.execute("""
        INSERT INTO stg_vendors_clean (
            vendor_key,
            vendor_id,
            vendor_code,
            vendor_name,
            status
        )
        VALUES (?, ?, ?, ?, ?);
    """, (
        vendor_id,
        vendor_id,
        vendor_code,
        vendor_name,
        status
    ))
