def transform_throughput(raw, stg, ex, site_map, wo_map, machine_map, operator_map):
    tid, site_id, wo_id, machine_id, operator_id, units, scrap, ts, shift = raw

    # FK validation
    if site_id not in site_map: ex.execute(...); return
    if wo_id not in wo_map: ex.execute(...); return
    if machine_id not in machine_map: ex.execute(...); return
    if operator_id not in operator_map: ex.execute(...); return

    # Business rule: units must be >= 0
    if units < 0:
        ex.execute(...); return

    ts = ts.replace(" ", "T")

    stg.execute("""
        INSERT INTO stg_throughput_clean (
            throughput_key, throughput_id, site_key, wo_key,
            machine_key, operator_key, units_produced,
            scrap_units, timestamp, shift_code
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (tid, tid, site_map[site_id], wo_map[wo_id],
          machine_map[machine_id], operator_map[operator_id],
          units, scrap, ts, shift))
