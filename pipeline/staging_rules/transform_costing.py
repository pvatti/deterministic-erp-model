def transform_costing(raw, stg, ex, item_map, site_map):
    cost_id, item_id, site_id, std_cost, ts, updated_by = raw

    # 1. FK validation
    if item_id not in item_map:
        ex.execute(...); return
    if site_id not in site_map:
        ex.execute(...); return

    # 2. Business rule validation
    if std_cost < 0:
        ex.execute(...); return

    # 3. Normalize
    ts = ts.replace(" ", "T") if ts else None

    # 4. Canonicalize
    updated_by = updated_by.strip() if updated_by else None

    # 5. Insert
    stg.execute("""
        INSERT INTO stg_costing_clean (
            cost_key, cost_id, item_key, site_key,
            standard_cost, last_updated_at, updated_by
        ) VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (cost_id, cost_id, item_map[item_id], site_map[site_id],
          std_cost, ts, updated_by))
