def transform_receipt(raw, stg, ex, po_line_map):
    receipt_id, po_line_id, qty, ts, received_by = raw

    if po_line_id not in po_line_map: ex.execute(...); return
    if qty <= 0: ex.execute(...); return

    ts = ts.replace(" ", "T")

    stg.execute("""
        INSERT INTO stg_receipts_clean (
            receipt_key, receipt_id, po_line_key, received_quantity, timestamp, received_by
        ) VALUES (?, ?, ?, ?, ?, ?);
    """, (receipt_id, receipt_id, po_line_map[po_line_id], qty, ts, received_by))
