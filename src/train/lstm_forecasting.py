import os
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

from pathlib import Path
from dotenv import load_dotenv


try:
    from dotenv import load_dotenv
    _root = Path(__file__).resolve().parent.parent.parent
    load_dotenv(_root / ".env")
except ImportError:
    pass

DB_URL = os.getenv("DB_URL")

def create_sequences(data, seq_length=7):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i + seq_length])
        y.append(data[i + seq_length])
    return np.array(X), np.array(y)


def main():
    engine = create_engine(DB_URL)

    df = pd.read_sql("SELECT * FROM mart_daily_sales ORDER BY date", engine)

    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)

    values = df["revenue"].values.reshape(-1, 1)

    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(values)

    seq_length = 7
    X, y = create_sequences(scaled, seq_length)

    split = int(len(X) * 0.8)

    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    model = Sequential([
        LSTM(50, activation='relu', input_shape=(seq_length, 1)),
        Dense(1)
    ])

    model.compile(optimizer='adam', loss='mse')

    model.fit(X_train, y_train, epochs=10, batch_size=16, verbose=1)

    preds = model.predict(X_test)

    preds = scaler.inverse_transform(preds)
    y_test = scaler.inverse_transform(y_test)

    rmse = np.sqrt(((preds - y_test) ** 2).mean())

    print("LSTM RMSE:", rmse)


if __name__ == "__main__":
    main()