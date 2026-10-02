DROP VIEW IF EXISTS sm_purchase_orders;

CREATE VIEW sm_purchase_orders AS
SELECT
    po.vendor_id,
    v.vendor_code,
    v.vendor_name,
    po.site_id,
    s.site_code,
    po.item_id,
    i.item_sku,
    i.item_description,
    po.po_number,
    po.order_date,
    po.promised_date,
    po.received_date,
    po.ordered_qty,
    po.received_qty,
    po.open_qty,
    (julianday(po.received_date) - julianday(po.order_date)) AS po_cycle_time_days
FROM fact_purchase_order po
JOIN dim_vendor v ON po.vendor_id = v.vendor_id
JOIN dim_sites s ON po.site_id = s.site_id
JOIN dim_item i ON po.item_id = i.item_id;
