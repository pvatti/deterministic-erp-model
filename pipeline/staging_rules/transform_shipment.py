def transform_shipping(raw, stg, ex):
    """
    RAW: shipping_raw
        shipment_id, order_id, shipped_quantity,
        timestamp, carrier, tracking_number

    STAGING: stg_shipping_clean
        shipment_key, shipment_id, order_key,
        shipped_quantity, timestamp, carrier, tracking_number
    """

    shipment_id, order_id, shipped_quantity, timestamp, carrier, tracking_number = raw

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
            VALUES ('shipping_raw', ?, 'Missing order', 'high',
                    'order_id not found in stg_customer_orders_clean', datetime('now'),
                    'transform_shipping');
        """, (shipment_id,))
        return
    order_key = order_row[0]

    # Normalize
    carrier = carrier.strip() if carrier else None
    tracking_number = tracking_number.strip() if tracking_number else None

    stg.execute("""
        INSERT INTO stg_shipping_clean (
            shipment_key,
            shipment_id,
            order_key,
            shipped_quantity,
            timestamp,
            carrier,
            tracking_number
        )
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (
        shipment_id,
        shipment_id,
        order_key,
        shipped_quantity,
        timestamp,
        carrier,
        tracking_number
    ))
