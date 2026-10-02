DROP VIEW IF EXISTS sm_ar;

CREATE VIEW sm_ar AS
SELECT
    f.customer_id,
    c.customer_code,
    c.customer_name,
    f.invoice_number,
    f.invoice_date,
    f.net_revenue AS invoice_amount,
    f.net_revenue
        - COALESCE(p.amount_paid, 0) AS open_amount,
    CASE
        WHEN julianday('now') - julianday(f.invoice_date) <= 30 THEN '0-30'
        WHEN julianday('now') - julianday(f.invoice_date) <= 60 THEN '31-60'
        WHEN julianday('now') - julianday(f.invoice_date) <= 90 THEN '61-90'
        ELSE '90+'
    END AS aging_bucket
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_id = c.customer_id
LEFT JOIN sm_ar_payments p
    ON p.invoice_number = f.invoice_number;
