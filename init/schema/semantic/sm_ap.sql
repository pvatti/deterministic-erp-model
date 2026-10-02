DROP VIEW IF EXISTS sm_ap;

CREATE VIEW sm_ap AS
SELECT
    ap.invoice_date,
    ap.due_date,
    dv.vendor_code,
    dv.vendor_name,
    ap.invoice_amount,
    ap.open_amount,
    -- Business metric
    (julianday('now') - julianday(ap.due_date)) AS days_past_due
FROM gold_ap ap
LEFT JOIN gold_vendors dv ON ap.vendor_key = dv.vendor_key;
