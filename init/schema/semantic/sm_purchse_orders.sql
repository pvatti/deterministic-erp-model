CREATE VIEW sm_purchase_orders AS
SELECT
    po.order_date,
    po.promised_date,
    po.received_date,
    dv.vendor_code,
    dv.vendor_name,
    ds.site_code,
    di.item_code,
    po.ordered_qty,
    po.received_qty,
    po.open_qty,
    -- Business metric
    (julianday(po.received_date) - julianday(po.order_date)) AS po_cycle_time_days
FROM gold_po_lines po
LEFT JOIN gold_vendors dv ON po.vendor_key = dv.vendor_key
LEFT JOIN gold_sites ds ON po.site_key = ds.site_key
LEFT JOIN gold_items di ON po.item_key = di.item_key;
