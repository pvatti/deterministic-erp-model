def transform_item(raw, stg, ex):
    item_id, sku, name, item_type, uom, status = raw

    # Validation
    if item_type not in ("FG", "WIP", "RM"):
        ex.execute("""
            INSERT INTO stg_exceptions (source_table, source_record_id, exception_type,
                                        severity, description, timestamp, rule_name)
            VALUES ('items', ?, 'Invalid item_type', 'high',
                    'Item type must be FG/WIP/RM', datetime('now'), 'transform_item');
        """, (item_id,))
        return

    # Normalization
    uom = uom.upper().strip()

    stg.execute("""
        INSERT INTO stg_items_clean (item_key, item_id, item_sku, item_name, item_type, uom, status)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (item_id, item_id, sku.strip(), name.strip(), item_type, uom, status))
