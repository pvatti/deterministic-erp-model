def transform_customers(raw, stg, ex):
    """
    RAW: customers
        customer_id, customer_code, customer_name, status

    STAGING: stg_customers_clean
        customer_key, customer_id, customer_code, customer_name, status
    """
    customer_id, customer_code, customer_name, status = raw

    if status not in ("active", "inactive"):
        ex.execute("""
            INSERT INTO stg_exceptions (
                source_table, source_record_id, exception_type,
                severity, description, timestamp, rule_name
            )
            VALUES ('customers', ?, 'Invalid status', 'high',
                    'Status must be active or inactive', datetime('now'), 'transform_customers');
        """, (customer_id,))
        return

    customer_code = customer_code.strip()
    customer_name = customer_name.strip()

    stg.execute("""
        INSERT INTO stg_customers_clean (
            customer_key,
            customer_id,
            customer_code,
            customer_name,
            status
        )
        VALUES (?, ?, ?, ?, ?);
    """, (
        customer_id,
        customer_id,
        customer_code,
        customer_name,
        status
    ))
