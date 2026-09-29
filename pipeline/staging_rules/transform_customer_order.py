def transform_customer_order(raw, stg, ex, customer_map):
    order_id, customer_id, order_date, required_date, status, created_by = raw

    # 1. FK validation
    if customer_id not in customer_map:
        ex.execute("""
            INSERT INTO stg_exceptions (source_table, source_record_id, exception_type,
                                        severity, description, timestamp, rule_name)
            VALUES ('customer_orders_raw', ?, 'Missing customer', 'high',
                    'Customer ID not found in dim_customers', datetime('now'), 'transform_customer_order');
        """, (order_id,))
        return

    # 2. Business rule validation
    if status not in ("open", "closed", "cancelled"):
        ex.execute("""
            INSERT INTO stg_exceptions (source_table, source_record_id, exception_type,
                                        severity, description, timestamp, rule_name)
            VALUES ('customer_orders_raw', ?, 'Invalid status', 'medium',
                    'Order status must be open/closed/cancelled', datetime('now'), 'transform_customer_order');
        """, (order_id,))
        return

    # 3. Normalize timestamps
    order_date = order_date.replace(" ", "T")
    required_date = required_date.replace(" ", "T") if required_date else None

    # 4. Canonicalize
    status = status.lower().strip()

    # 5. Insert
    stg.execute("""
        INSERT INTO stg_customer_orders_clean (
            order_key, order_id, customer_key, order_date,
            required_date, status, created_by
        ) VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (order_id, order_id, customer_map[customer_id], order_date,
          required_date, status, created_by))
