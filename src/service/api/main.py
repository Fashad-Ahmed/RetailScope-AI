import os
from pathlib import Path

import pandas as pd
from fastapi import FastAPI
from sqlalchemy import create_engine

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[3]
load_dotenv(ROOT_DIR / ".env")

DB_URL = os.getenv("DB_URL")

if DB_URL is None:
    raise ValueError("DB_URL is not set. Check your .env file.")

def get_engine():
    return create_engine(DB_URL)


app = FastAPI(title="Retail Intelligence API")


@app.get("/")
def root():
    return {"message": "Retail Intelligence Platform API"}


@app.get("/segments")
def get_segments():
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM mart_customer_segments LIMIT 100", engine)
    return df.to_dict(orient="records")


@app.get("/recommendations")
def get_recommendations():
    engine = get_engine()
    df = pd.read_sql("""
        SELECT * FROM mart_association_rules
        ORDER BY lift DESC
        LIMIT 20
    """, engine)
    return df.to_dict(orient="records")

@app.get("/forecast")
def get_forecast():
    engine = get_engine()
    df = pd.read_sql("""
        SELECT * FROM mart_prophet_forecast
        ORDER BY ds DESC
        LIMIT 30
    """, engine)
    return df.to_dict(orient="records")


@app.get("/models")
def get_models():
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM mart_model_performance", engine)
    return df.to_dict(orient="records")