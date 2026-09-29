def transform_customer_order_line(raw, stg, ex, order_map, item_map):
    order_line_id, order_id, item_id, qty, uom, notes = raw

    # 1. FK validation
    if order_id not in order_map:
        ex.execute(...); return
    if item_id not in item_map:
        ex.execute(...); return

    # 2. Business rule validation
    if qty <= 0:
        ex.execute(...); return

    # 3. Normalize
    uom = uom.upper().strip()

    # 4. Canonicalize
    # (no special canonicalization needed here)

    # 5. Insert
    stg.execute("""
        INSERT INTO stg_customer_order_lines_clean (
            order_line_key, order_line_id, order_key, item_key,
            ordered_quantity, uom, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (order_line_id, order_line_id, order_map[order_id],
          item_map[item_id], qty, uom, notes))
