def transform_ar(raw, stg, ex):
    """
    RAW: ar_raw
        ar_id, customer_id, amount, due_date, status

    STAGING: stg_ar_clean
        ar_key, ar_id, customer_key, amount, due_date, status
    """

    ar_id, customer_id, amount, due_date, status = raw

    # Lookup customer_key
    customer_row = stg.execute(
        "SELECT customer_key FROM stg_customers_clean WHERE customer_id = ?;",
        (customer_id,)
    ).fetchone()
    if customer_row is None:
        ex.execute("""
            INSERT INTO stg_exceptions (
                source_table, source_record_id, exception_type, severity,
                description, timestamp, rule_name
            )
            VALUES ('ar_raw', ?, 'Missing customer', 'high',
                    'customer_id not found in stg_customers_clean', datetime('now'),
                    'transform_ar');
        """, (ar_id,))
        return
    customer_key = customer_row[0]

    # Normalize
    status = status.strip() if status else None

    stg.execute("""
        INSERT INTO stg_ar_clean (
            ar_key,
            ar_id,
            customer_key,
            amount,
            due_date,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?);
    """, (
        ar_id,
        ar_id,
        customer_key,
        amount,
        due_date,
        status
    ))
