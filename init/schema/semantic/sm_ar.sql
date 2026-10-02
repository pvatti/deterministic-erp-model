CREATE VIEW sm_ar AS
SELECT
    ar.invoice_date,
    ar.due_date,
    dc.customer_code,
    dc.customer_name,
    ar.invoice_amount,
    ar.open_amount,
    -- Business metric
    (julianday('now') - julianday(ar.due_date)) AS days_past_due
FROM gold_ar ar
LEFT JOIN gold_customers dc ON ar.customer_key = dc.customer_key;
