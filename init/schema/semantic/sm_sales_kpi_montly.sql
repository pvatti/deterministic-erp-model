DROP VIEW IF EXISTS sm_sales_kpi_monthly;

CREATE VIEW sm_sales_kpi_monthly AS
SELECT
    strftime('%Y-%m', invoice_date) AS fiscal_month,
    SUM(net_revenue) AS monthly_revenue,
    SUM(sold_qty) AS monthly_units,
    SUM(discount) AS monthly_discount
FROM fact_sales
GROUP BY strftime('%Y-%m', invoice_date);
