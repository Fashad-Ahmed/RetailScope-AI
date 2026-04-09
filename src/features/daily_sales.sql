DROP TABLE IF EXISTS mart_daily_sales;

CREATE TABLE mart_daily_sales AS
SELECT
    invoice_date AS date,
    SUM(total_amount) AS revenue,
    COUNT(DISTINCT invoice_no) AS orders
FROM fact_sales
GROUP BY invoice_date
ORDER BY date;