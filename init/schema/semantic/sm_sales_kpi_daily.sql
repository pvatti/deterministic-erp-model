DROP VIEW IF EXISTS sm_sales_kpi_daily;

CREATE VIEW sm_sales_kpi_daily AS
SELECT
    invoice_date,
    SUM(net_revenue) AS daily_revenue,
    SUM(sold_qty) AS daily_units,
    SUM(discount) AS daily_discount
FROM fact_sales
GROUP BY invoice_date;
