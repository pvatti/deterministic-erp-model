def transform_po(raw, stg, ex, vendor_map):
    po_id, vendor_id, po_date, status, created_by = raw

    # 1. FK validation
    if vendor_id not in vendor_map:
        ex.execute(...); return

    # 2. Business rule validation
    if status not in ("open", "closed", "cancelled"):
        ex.execute(...); return

    # 3. Normalize
    po_date = po_date.replace(" ", "T")

    # 4. Canonicalize
    status = status.lower().strip()

    # 5. Insert
    stg.execute("""
        INSERT INTO stg_po_clean (
            po_key, po_id, vendor_key, po_date, status, created_by
        ) VALUES (?, ?, ?, ?, ?, ?);
    """, (po_id, po_id, vendor_map[vendor_id], po_date, status, created_by))
