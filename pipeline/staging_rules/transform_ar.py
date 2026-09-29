def transform_ar(raw, stg, ex, customer_map):
    ar_id, customer_id, amount, due_date, status = raw

    # 1. FK validation
    if customer_id not in customer_map:
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
        INSERT INTO stg_ar_clean (
            ar_key, ar_id, customer_key, amount, due_date, status
        ) VALUES (?, ?, ?, ?, ?, ?);
    """, (ar_id, ar_id, customer_map[customer_id], amount, due_date, status))
