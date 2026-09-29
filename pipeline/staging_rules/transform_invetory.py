def transform_inventory(raw, stg, ex, site_map, item_map):
    inv_id, site_id, item_id, qty, loc, ts, user, notes = raw

    # FK validation
    if site_id not in site_map:
        ex.execute(...); return
    if item_id not in item_map:
        ex.execute(...); return

    # Business rule: quantity must be >= 0
    if qty < 0:
        ex.execute(...); return

    # Timestamp normalization
    ts = ts.replace(" ", "T")

    stg.execute("""
        INSERT INTO stg_inventory_clean (
            inventory_key, inventory_id, site_key, item_key,
            quantity_on_hand, location_code, last_updated_at, last_updated_by
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, (inv_id, inv_id, site_map[site_id], item_map[item_id], qty, loc, ts, user))
