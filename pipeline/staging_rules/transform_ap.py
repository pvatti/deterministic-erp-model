def transform_ap(raw, stg, ex, vendor_map):
    ap_id, vendor_id, amount, due_date, status = raw

    # 1. FK validation
    if vendor_id not in vendor_map:
        ex.execute(...); return

    # 2. Business rule validation
    if amount < 0:
        ex.execute(...); return

    if status not in ("open", "paid", "cancelled"):
        ex.execute(...); return

    # 3. Normalize
    due_date = due_date.replace(" ", "T") if due_date else None

    # 4. Canonicalize
    status = status.lower().strip()

    # 5. Insert
    stg.execute("""
        INSERT INTO stg_ap_clean (
            ap_key, ap_id, vendor_key, amount, due_date, status
        ) VALUES (?, ?, ?, ?, ?, ?);
    """, (ap_id, ap_id, vendor_map[vendor_id], amount, due_date, status))
