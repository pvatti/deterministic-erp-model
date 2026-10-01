def transform_machines(raw, stg, ex):
    """
    RAW: machines
        machine_id, site_id, machine_code, machine_name, status

    STAGING: stg_machines_clean
        machine_key, machine_id, machine_code, machine_name, site_id, status
    """
    machine_id, site_id, machine_code, machine_name, status = raw

    if status not in ("active", "inactive"):
        ex.execute("""
            INSERT INTO stg_exceptions (
                source_table, source_record_id, exception_type,
                severity, description, timestamp, rule_name
            )
            VALUES ('machines', ?, 'Invalid status', 'high',
                    'Status must be active or inactive', datetime('now'), 'transform_machines');
        """, (machine_id,))
        return

    # Ensure site exists in stg_sites_clean
    site_row = stg.execute(
        "SELECT site_key FROM stg_sites_clean WHERE site_id = ?;",
        (site_id,)
    ).fetchone()
    if site_row is None:
        ex.execute("""
            INSERT INTO stg_exceptions (
                source_table, source_record_id, exception_type,
                severity, description, timestamp, rule_name
            )
            VALUES ('machines', ?, 'Missing site', 'high',
                    'Referenced site_id not found in stg_sites_clean', datetime('now'), 'transform_machines');
        """, (machine_id,))
        return

    machine_code = machine_code.strip()
    machine_name = machine_name.strip()

    stg.execute("""
        INSERT INTO stg_machines_clean (
            machine_key,
            machine_id,
            machine_code,
            machine_name,
            site_id,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?);
    """, (
        machine_id,
        machine_id,
        machine_code,
        machine_name,
        site_id,
        status
    ))
