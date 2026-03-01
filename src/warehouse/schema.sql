-- Dimension: Customer
CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id BIGINT PRIMARY KEY,
    country TEXT
);

-- Dimension: Product
CREATE TABLE IF NOT EXISTS dim_product (
    stock_code TEXT PRIMARY KEY,
    description TEXT
);

-- Dimension: Date
CREATE TABLE IF NOT EXISTS dim_date (
    date DATE PRIMARY KEY,
    year INT,
    month INT,
    day INT,
    day_of_week INT,
    week INT
);

-- Fact Table: Sales
CREATE TABLE IF NOT EXISTS fact_sales (
    invoice_no TEXT,
    invoice_date DATE,
    customer_id BIGINT,
    stock_code TEXT,
    quantity INT,
    unit_price FLOAT,
    total_amount FLOAT,
    country TEXT,
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
    FOREIGN KEY (stock_code) REFERENCES dim_product(stock_code),
    FOREIGN KEY (invoice_date) REFERENCES dim_date(date)
);