def transform_scrap(raw, stg, ex, site_map, item_map, operator_map):
    scrap_id, site_id, item_id, qty, reason, ts, operator_id = raw

    if site_id not in site_map: ex.execute(...); return
    if item_id not in item_map: ex.execute(...); return
    if operator_id not in operator_map: ex.execute(...); return

    if qty < 0:
        ex.execute(...); return

    ts = ts.replace(" ", "T")

    stg.execute("""
        INSERT INTO stg_scrap_clean (
            scrap_key, scrap_id, site_key, item_key,
            quantity, reason, timestamp, operator_key
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, (scrap_id, scrap_id, site_map[site_id], item_map[item_id],
          qty, reason, ts, operator_map[operator_id]))
