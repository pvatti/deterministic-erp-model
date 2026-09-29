def transform_site(raw, stg, ex):
    site_id, site_code, site_name, region, status = raw

    # Validation
    if status not in ("active", "inactive"):
        ex.execute("""
            INSERT INTO stg_exceptions (source_table, source_record_id, exception_type,
                                        severity, description, timestamp, rule_name)
            VALUES ('sites', ?, 'Invalid status', 'high',
                    'Status must be active/inactive', datetime('now'), 'transform_site');
        """, (site_id,))
        return

    # Canonicalization
    region = region.strip().title() if region else None

    stg.execute("""
        INSERT INTO stg_sites_clean (site_key, site_id, site_code, site_name, region, status)
        VALUES (?, ?, ?, ?, ?, ?);
    """, (site_id, site_id, site_code.strip(), site_name.strip(), region, status))
