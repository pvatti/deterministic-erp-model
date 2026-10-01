def transform_throughput(raw, stg, ex):
    """
    RAW: throughput_raw
        throughput_id, site_id, work_order_id, machine_id,
        operator_id, units_produced, scrap_units,
        timestamp, shift_code, notes

    STAGING: stg_throughput_clean
        throughput_key, throughput_id, site_key, wo_key,
        machine_key, operator_key, units_produced,
        scrap_units, timestamp, shift_code
    """

    (throughput_id, site_id, work_order_id, machine_id, operator_id,
     units_produced, scrap_units, timestamp, shift_code, notes) = raw

    # Lookup site_key
    site_key = stg.execute(
        "SELECT site_key FROM stg_sites_clean WHERE site_id = ?;",
        (site_id,)
    ).fetchone()
    if site_key is None:
        ex.execute("""
            INSERT INTO stg_exceptions (
                source_table, source_record_id, exception_type, severity,
                description, timestamp, rule_name
            )
            VALUES ('throughput_raw', ?, 'Missing site', 'high',
                    'site_id not found in stg_sites_clean', datetime('now'),
                    'transform_throughput');
        """, (throughput_id,))
        return
    site_key = site_key[0]

    # Lookup wo_key
    wo_key = stg.execute(
        "SELECT wo_key FROM stg_work_orders_clean WHERE work_order_id = ?;",
        (work_order_id,)
    ).fetchone()
    if wo_key is None:
        ex.execute("""
            INSERT INTO stg_exceptions (
                source_table, source_record_id, exception_type, severity,
                description, timestamp, rule_name
            )
            VALUES ('throughput_raw', ?, 'Missing work order', 'high',
                    'work_order_id not found in stg_work_orders_clean', datetime('now'),
                    'transform_throughput');
        """, (throughput_id,))
        return
    wo_key = wo_key[0]

    # Lookup machine_key
    machine_key = stg.execute(
        "SELECT machine_key FROM stg_machines_clean WHERE machine_id = ?;",
        (machine_id,)
    ).fetchone()
    if machine_key is None:
        ex.execute("""
            INSERT INTO stg_exceptions (
                source_table, source_record_id, exception_type, severity,
                description, timestamp, rule_name
            )
            VALUES ('throughput_raw', ?, 'Missing machine', 'high',
                    'machine_id not found in stg_machines_clean', datetime('now'),
                    'transform_throughput');
        """, (throughput_id,))
        return
    machine_key = machine_key[0]

    # Lookup operator_key
    operator_key = stg.execute(
        "SELECT operator_key FROM stg_operators_clean WHERE operator_id = ?;",
        (operator_id,)
    ).fetchone()
    if operator_key is None:
        ex.execute("""
            INSERT INTO stg_exceptions (
                source_table, source_record_id, exception_type, severity,
                description, timestamp, rule_name
            )
            VALUES ('throughput_raw', ?, 'Missing operator', 'high',
                    'operator_id not found in stg_operators_clean', datetime('now'),
                    'transform_throughput');
        """, (throughput_id,))
        return
    operator_key = operator_key[0]

    # Normalize
    shift_code = shift_code.strip() if shift_code else None

    stg.execute("""
        INSERT INTO stg_throughput_clean (
            throughput_key,
            throughput_id,
            site_key,
            wo_key,
            machine_key,
            operator_key,
            units_produced,
            scrap_units,
            timestamp,
            shift_code
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        throughput_id,
        throughput_id,
        site_key,
        wo_key,
        machine_key,
        operator_key,
        units_produced,
        scrap_units,
        timestamp,
        shift_code
    ))
