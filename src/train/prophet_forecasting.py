import os
import pandas as pd
from sqlalchemy import create_engine
from prophet import Prophet

from pathlib import Path

try:
    from dotenv import load_dotenv
    _root = Path(__file__).resolve().parent.parent.parent
    load_dotenv(_root / ".env")
except ImportError:
    pass


DB_URL = os.getenv("DB_URL")


def main():
    engine = create_engine(DB_URL)

    df = pd.read_sql("SELECT * FROM mart_daily_sales ORDER BY date", engine)

    df.rename(columns={"date": "ds", "revenue": "y"}, inplace=True)

    model = Prophet()
    model.fit(df)

    future = model.make_future_dataframe(periods=30)

    forecast = model.predict(future)

    print(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail())

    forecast[["ds", "yhat"]].to_sql(
        "mart_prophet_forecast",
        engine,
        if_exists="replace",
        index=False
    )

    print("Prophet forecast saved")


if __name__ == "__main__":
    main()