from pathlib import Path
import os

import pandas as pd
import numpy as np
from sqlalchemy import create_engine

from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from xgboost import XGBRegressor

try:
    from dotenv import load_dotenv
    _root = Path(__file__).resolve().parent.parent.parent
    load_dotenv(_root / ".env")
except ImportError:
    pass

DB_URL = os.getenv("DB_URL")

def create_lag_features(df, lags=7):
    for lag in range(1, lags + 1):
        df[f"lag_{lag}"] = df["revenue"].shift(lag)
    return df


def main():
    engine = create_engine(DB_URL)

    df = pd.read_sql("SELECT * FROM mart_daily_sales ORDER BY date", engine)

    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)

    print("Loaded time series:", df.shape)

    train_size = int(len(df) * 0.8)

    train = df.iloc[:train_size]
    test = df.iloc[train_size:]

    print("\nTraining ARIMA...")

    arima_model = ARIMA(train["revenue"], order=(5, 1, 0))
    arima_fit = arima_model.fit()

    arima_pred = arima_fit.forecast(steps=len(test))

    arima_rmse = np.sqrt(mean_squared_error(test["revenue"], arima_pred))
    print("ARIMA RMSE:", arima_rmse)

    print("\nTraining XGBoost...")

    df_lag = create_lag_features(df.copy())
    df_lag.dropna(inplace=True)

    X = df_lag.drop(columns=["revenue"])
    y = df_lag["revenue"]

    split = int(len(X) * 0.8)

    X_train, X_test = X.iloc[:split], X.iloc[split:]
    y_train, y_test = y.iloc[:split], y.iloc[split:]

    xgb = XGBRegressor(n_estimators=100, learning_rate=0.1)
    xgb.fit(X_train, y_train)

    xgb_pred = xgb.predict(X_test)

    xgb_rmse = np.sqrt(mean_squared_error(y_test, xgb_pred))
    print("XGBoost RMSE:", xgb_rmse)
    
    results = pd.DataFrame({
        "model": ["ARIMA", "XGBoost"],
        "rmse": [arima_rmse, xgb_rmse]
    })

    results.to_sql(
        "mart_model_performance",
        engine,
        if_exists="replace",
        index=False
    )

    print("\nModel performance saved")


if __name__ == "__main__":
    main()