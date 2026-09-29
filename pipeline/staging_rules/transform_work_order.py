def transform_work_order(raw, stg, ex, site_map, item_map):
    wo_id, site_id, item_id, qty, start, end, status, created_by = raw

    if site_id not in site_map:
        ex.execute(...); return
    if item_id not in item_map:
        ex.execute(...); return

    # Business rule: planned quantity must be > 0
    if qty <= 0:
        ex.execute(...); return

    # Normalize timestamps
    start = start.replace(" ", "T") if start else None
    end = end.replace(" ", "T") if end else None

    stg.execute("""
        INSERT INTO stg_work_orders_clean (
            wo_key, work_order_id, site_key, item_key,
            planned_quantity, scheduled_start, scheduled_end,
            status, created_by
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (wo_id, wo_id, site_map[site_id], item_map[item_id], qty, start, end, status, created_by))
