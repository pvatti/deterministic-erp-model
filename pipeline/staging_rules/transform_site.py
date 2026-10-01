def transform_sites(raw, stg, ex):
    """
    RAW: sites
        site_id, site_code, site_name, region, status

    STAGING: stg_sites_clean
        site_key, site_id, site_code, site_name, region, status
    """
    site_id, site_code, site_name, region, status = raw

    # Validate status
    if status not in ("active", "inactive"):
        ex.execute("""
            INSERT INTO stg_exceptions (
                source_table, source_record_id, exception_type,
                severity, description, timestamp, rule_name
            )
            VALUES ('sites', ?, 'Invalid status', 'high',
                    'Status must be active or inactive', datetime('now'), 'transform_sites');
        """, (site_id,))
        return

    # Normalize
    site_code = site_code.strip()
    site_name = site_name.strip()
    region = region.strip() if region else None

    stg.execute("""
        INSERT INTO stg_sites_clean (
            site_key,
            site_id,
            site_code,
            site_name,
            region,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?);
    """, (
        site_id,        # surrogate key = raw id
        site_id,
        site_code,
        site_name,
        region,
        status
    ))
