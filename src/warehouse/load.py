from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text

DB_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/retaildw"
PARQUET_PATH = Path("data/clean/transactions.parquet")

def main():
    df = pd.read_parquet(PARQUET_PATH)
    print("Parquet loaded:", df.shape)
    print("Columns:", list(df.columns))

    # Ensure correct dtypes
    df["invoice_date"] = pd.to_datetime(df["invoice_date"])
    df["customer_id"] = df["customer_id"].astype("int64")
    df["quantity"] = df["quantity"].astype("int64")

    # Fact table data (invoice_date as DATE)
    fact = df.copy()
    fact["invoice_date"] = fact["invoice_date"].dt.date

    engine = create_engine(DB_URL)

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE fact_sales"))
        fact.to_sql(
            "fact_sales",
            conn,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=20000
        )

    print("Loaded rows into fact_sales:", len(fact))

if __name__ == "__main__":
    main()