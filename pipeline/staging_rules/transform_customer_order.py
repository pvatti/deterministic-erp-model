def transform_customer_orders(raw, stg, ex):
    """
    RAW: customer_orders_raw
        order_id, customer_id, order_date,
        required_date, status, created_by

    STAGING: stg_customer_orders_clean
        order_key, order_id, customer_key,
        order_date, required_date, status, created_by
    """

    order_id, customer_id, order_date, required_date, status, created_by = raw

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
            VALUES ('customer_orders_raw', ?, 'Missing customer', 'high',
                    'customer_id not found in stg_customers_clean', datetime('now'),
                    'transform_customer_orders');
        """, (order_id,))
        return
    customer_key = customer_row[0]

    # Normalize
    status = status.strip() if status else None
    created_by = created_by.strip() if created_by else None

    stg.execute("""
        INSERT INTO stg_customer_orders_clean (
            order_key,
            order_id,
            customer_key,
            order_date,
            required_date,
            status,
            created_by
        )
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (
        order_id,
        order_id,
        customer_key,
        order_date,
        required_date,
        status,
        created_by
    ))
