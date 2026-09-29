def transform_vendor(raw, stg, ex):
    vendor_id, code, name, status = raw

    if status not in ("active", "inactive"):
        ex.execute(...)

    stg.execute("""
        INSERT INTO stg_vendors_clean (vendor_key, vendor_id, vendor_code, vendor_name, status)
        VALUES (?, ?, ?, ?, ?);
    """, (vendor_id, vendor_id, code.strip(), name.strip(), status))
