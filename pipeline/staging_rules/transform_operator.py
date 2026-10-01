def transform_operators(raw, stg, ex):
    """
    RAW: operators
        operator_id, site_id, operator_code, operator_name, role

    STAGING: stg_operators_clean
        operator_key, operator_id, operator_code, operator_name, role, site_id
    """
    operator_id, site_id, operator_code, operator_name, role = raw

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
            VALUES ('operators', ?, 'Missing site', 'high',
                    'Referenced site_id not found in stg_sites_clean', datetime('now'), 'transform_operators');
        """, (operator_id,))
        return

    operator_code = operator_code.strip()
    operator_name = operator_name.strip()
    role = role.strip() if role else None

    stg.execute("""
        INSERT INTO stg_operators_clean (
            operator_key,
            operator_id,
            operator_code,
            operator_name,
            role,
            site_id
        )
        VALUES (?, ?, ?, ?, ?, ?);
    """, (
        operator_id,
        operator_id,
        operator_code,
        operator_name,
        role,
        site_id
    ))
