def transform_shipment(raw, stg, ex, order_map):
    shipment_id, order_id, qty, ts, carrier, tracking = raw

    # 1. FK validation
    if order_id not in order_map:
        ex.execute(...); return

    # 2. Business rule validation
    if qty <= 0:
        ex.execute(...); return

    # 3. Normalize
    ts = ts.replace(" ", "T")

    # 4. Canonicalize
    carrier = carrier.strip() if carrier else None

    # 5. Insert
    stg.execute("""
        INSERT INTO stg_shipping_clean (
            shipment_key, shipment_id, order_key,
            shipped_quantity, timestamp, carrier, tracking_number
        ) VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (shipment_id, shipment_id, order_map[order_id],
          qty, ts, carrier, tracking))
