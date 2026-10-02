DROP VIEW IF EXISTS sm_ap;

CREATE VIEW sm_ap AS
SELECT
    po.vendor_id,
    v.vendor_code,
    v.vendor_name,
    po.po_number,
    po.order_date,
    po.extended_price AS invoice_amount,
    po.extended_price
        - COALESCE(p.amount_paid, 0) AS open_amount,
    CASE
        WHEN julianday('now') - julianday(po.order_date) <= 30 THEN '0-30'
        WHEN julianday('now') - julianday(po.order_date) <= 60 THEN '31-60'
        WHEN julianday('now') - julianday(po.order_date) <= 90 THEN '61-90'
        ELSE '90+'
    END AS aging_bucket
FROM fact_purchase_order po
JOIN dim_vendor v
    ON po.vendor_id = v.vendor_id
LEFT JOIN sm_ap_payments p
    ON p.po_number = po.po_number;
