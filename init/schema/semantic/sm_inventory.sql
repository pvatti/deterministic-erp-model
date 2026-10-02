CREATE VIEW sm_inventory AS
SELECT
    gi.snapshot_date,
    ds.site_code,
    ds.site_name,
    di.item_code,
    di.item_description,
    gi.on_hand_qty,
    gi.allocated_qty,
    gi.available_qty,
    -- Business metric
    CASE 
        WHEN gi.on_hand_qty = 0 THEN 0
        ELSE gi.available_qty * 1.0 / gi.on_hand_qty
    END AS availability_ratio
FROM gold_inventory gi
LEFT JOIN gold_sites ds ON gi.site_key = ds.site_key
LEFT JOIN gold_items di ON gi.item_key = di.item_key;
