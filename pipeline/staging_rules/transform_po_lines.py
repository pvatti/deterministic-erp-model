def transform_po_line(raw, stg, ex, po_map, item_map):
    po_line_id, po_id, item_id, qty, uom, notes = raw

    if po_id not in po_map: ex.execute(...); return
    if item_id not in item_map: ex.execute(...); return
    if qty <= 0: ex.execute(...); return

    uom = uom.upper().strip()

    stg.execute("""
        INSERT INTO stg_po_lines_clean (
            po_line_key, po_line_id, po_key, item_key, ordered_quantity, uom, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (po_line_id, po_line_id, po_map[po_id], item_map[item_id], qty, uom, notes))
