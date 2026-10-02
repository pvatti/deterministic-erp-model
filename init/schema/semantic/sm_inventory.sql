DROP VIEW IF EXISTS sm_inventory;

CREATE VIEW sm_inventory AS
SELECT
    i.item_id,
    i.item_sku,
    i.item_name,
    s.site_id,
    s.site_code,
    f.snapshot_date,
    f.on_hand_qty,
    f.on_hand_qty * i.standard_cost AS inventory_value
FROM fact_inventory_snapshot f
JOIN dim_item i
    ON f.item_id = i.item_id
JOIN dim_sites s
    ON f.site_id = s.site_id;
