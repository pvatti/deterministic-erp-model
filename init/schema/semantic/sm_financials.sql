DROP VIEW IF EXISTS sm_financials;

CREATE VIEW sm_financials AS
SELECT
    f.fiscal_year,
    f.fiscal_period,
    f.gl_account_code,
    f.gl_account_name,
    f.gl_category,
    f.gl_subcategory,
    SUM(f.amount) AS period_amount
FROM fact_financials f
GROUP BY
    f.fiscal_year,
    f.fiscal_period,
    f.gl_account_code,
    f.gl_account_name,
    f.gl_category,
    f.gl_subcategory;
