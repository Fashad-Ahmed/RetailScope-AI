import pandas as pd
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
RAW_PATH = _PROJECT_ROOT / "data" / "raw" / "online_retail.xlsx"
CLEAN_PATH = _PROJECT_ROOT / "data" / "clean" / "transactions.parquet"

def main():
    print("Loading raw dataset")
    
    df = pd.read_excel(RAW_PATH)

    print(f"Initial shape: {df.shape}")

    df.columns = df.columns.str.strip().str.lower()

    df.rename(columns={
        "invoice": "invoice_no",
        "stockcode": "stock_code",
        "description": "description",
        "quantity": "quantity",
        "invoicedate": "invoice_date",
        "price": "unit_price",
        "customer id": "customer_id",
        "country": "country"
    }, inplace=True)

    df = df.dropna(subset=["customer_id"])
    df = df[~df["invoice_no"].astype(str).str.startswith("C")]
    df = df[df["quantity"] > 0]
    df = df[df["unit_price"] > 0]

    df["invoice_date"] = pd.to_datetime(df["invoice_date"])
    df["customer_id"] = df["customer_id"].astype(int)
    df["total_amount"] = df["quantity"] * df["unit_price"]
    df["description"] = df["description"].astype(str).str.strip()

    # Ensure string columns for parquet (PyArrow rejects object dtype with mixed types)
    df["invoice_no"] = df["invoice_no"].astype(str)
    df["stock_code"] = df["stock_code"].astype(str)
    df["country"] = df["country"].astype(str)

    print(f"Cleaned shape: {df.shape}")

    CLEAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(CLEAN_PATH, index=False)

    print(f"Saved clean dataset to: {CLEAN_PATH}")


if __name__ == "__main__":
    main()