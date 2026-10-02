DROP VIEW IF EXISTS sm_financial_quarterly;

CREATE VIEW sm_financial_quarterly AS
SELECT
    f.fiscal_year,
    CASE
        WHEN f.fiscal_period BETWEEN 1 AND 3  THEN 'Q1'
        WHEN f.fiscal_period BETWEEN 4 AND 6  THEN 'Q2'
        WHEN f.fiscal_period BETWEEN 7 AND 9  THEN 'Q3'
        WHEN f.fiscal_period BETWEEN 10 AND 12 THEN 'Q4'
        ELSE 'UNKNOWN'
    END AS fiscal_quarter,
    f.gl_account_code,
    f.gl_account_name,
    f.gl_category,
    f.gl_subcategory,
    SUM(f.amount) AS quarter_amount
FROM fact_financials f
GROUP BY
    f.fiscal_year,
    fiscal_quarter,
    f.gl_account_code,
    f.gl_account_name,
    f.gl_category,
    f.gl_subcategory;
