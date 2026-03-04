DROP TABLE IF EXISTS mart_customer_rfm;

CREATE TABLE mart_customer_rfm AS
SELECT
    customer_id,
    MAX(invoice_date) AS last_purchase_date,
    COUNT(DISTINCT invoice_no) AS frequency,
    SUM(total_amount) AS monetary
FROM fact_sales
GROUP BY customer_id;


-- DROP TABLE IF EXISTS mart_customer_rfm;

-- CREATE TABLE mart_customer_rfm AS
-- SELECT
--     customer_id,
--     MAX(invoice_date) AS last_purchase_date,
--     COUNT(DISTINCT invoice_no) AS frequency,
--     SUM(total_amount) AS monetary,
--     DATE_PART('day', CURRENT_DATE - MAX(invoice_date)) AS recency
-- FROM fact_sales
-- GROUP BY customer_id;

DROP TABLE IF EXISTS mart_customer_rfm;

CREATE TABLE mart_customer_rfm AS
SELECT
    customer_id,
    MAX(invoice_date) AS last_purchase_date,
    COUNT(DISTINCT invoice_no) AS frequency,
    SUM(total_amount) AS monetary,
    CURRENT_DATE - MAX(invoice_date) AS recency
FROM fact_sales
GROUP BY customer_id;