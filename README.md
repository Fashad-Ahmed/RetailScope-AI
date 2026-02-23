

# RetailScope AI


### Note: The project is in progress 😊

## End to End Retail Intelligence Platform with Data Warehouse, Advanced Machine Learning, and Time-Series Forecasting

RetailScope AI is a production-oriented retail analytics platform designed to simulate a real-world decision intelligence system. The project integrates modern data engineering practices with classical and advanced machine learning techniques to extract actionable business insights from large-scale transactional retail data.

The platform follows a structured Data Mining lifecycle (CRISP-DM) and implements a complete pipeline from raw data ingestion to model deployment via REST APIs.

---

## Architecture Overview

The system follows a layered architecture:

Raw Data Layer
→ Data Cleaning (ETL)
→ Data Lake (Parquet)
→ Data Warehouse (PostgreSQL Star Schema)
→ Feature Engineering
→ Machine Learning & Time-Series Modeling
→ Model Serving (FastAPI)

Key architectural components:

* Data Lake: Cleaned datasets stored in Parquet format
* Data Warehouse: PostgreSQL star schema (fact and dimension tables)
* Feature Store: RFM features, lag features, rolling statistics
* ML Pipelines: Modular training and evaluation scripts
* API Layer: FastAPI-based model inference service

---

## Core Capabilities

### 1. Customer Analytics

* RFM (Recency, Frequency, Monetary) modeling
* Customer churn prediction
* Behavioral customer segmentation
* Feature importance and model evaluation

Models implemented:

* Logistic Regression
* Random Forest
* AdaBoost
* XGBoost (optional extension)

---

### 2. Market Basket Analysis

* Frequent itemset mining
* Association rule generation using Apriori
* Support, confidence, and lift analysis
* Actionable cross-selling insights

---

### 3. Time-Series Forecasting

Revenue and demand forecasting using:

* Baseline models (naive and seasonal naive)
* SARIMA (statistical forecasting)
* XGBoost with lag and rolling features
* LSTM (deep learning sequence modeling)

Evaluation methodology:

* Walk-forward validation
* TimeSeriesSplit
* MAE, RMSE, and MAPE metrics

---

## Data Engineering Design

### Data Lake

Cleaned transactional data is stored in Parquet format for:

* Efficient columnar storage
* Reduced I/O overhead
* Schema preservation
* Production-grade analytical workflows

### Data Warehouse

A PostgreSQL star schema includes:

Fact Table:

* fact_sales

Dimension Tables:

* dim_customer
* dim_product
* dim_date

Aggregated marts:

* mart_customer_rfm
* mart_daily_kpis

---

## Project Structure

```
retailscope-ai/
│
├── data/
│   ├── raw/
│   ├── clean/
│   └── features/
│
├── src/
│   ├── etl/
│   ├── warehouse/
│   ├── features/
│   ├── train/
│   ├── timeseries/
│   ├── service/
│   └── utils/
│
├── artifacts/
├── reports/
├── notebooks/
└── README.md
```

---

## Installation

### 1. Clone repository

```
git clone <repository-url>
cd retailscope-ai
```

### 2. Create virtual environment

```
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

## Running the Pipeline

### Step 1: Clean Raw Data

```
python -m src.etl.01_clean_transactions
```

### Step 2: Create Warehouse Schema

```
psql -f src/warehouse/01_schema.sql
```

### Step 3: Load Data into Warehouse

```
python -m src.warehouse.02_load
```

### Step 4: Feature Engineering

```
python -m src.features.01_build_rfm
```

### Step 5: Train Models

Churn:

```
python -m src.train.01_train_churn
```

Segmentation:

```
python -m src.train.02_segment_customers
```

Forecasting:

```
python -m src.timeseries.02_arima
python -m src.timeseries.03_xgb_forecast
python -m src.timeseries.04_lstm
```

### Step 6: Start API

```
uvicorn src.service.main:app --reload
```

---

## API Endpoints

* POST /predict_churn
* POST /segment_customer
* GET /rules?item=...
* GET /forecast/revenue?horizon=30

---

## Technologies Used

* Python
* Pandas, NumPy
* Scikit-learn
* XGBoost
* PyTorch
* Statsmodels
* PostgreSQL
* SQLAlchemy
* FastAPI
* Parquet

---

## Methodology

The project follows the CRISP-DM framework:

1. Business Understanding
2. Data Understanding
3. Data Preparation
4. Modeling
5. Evaluation
6. Deployment

Time-series models use proper walk-forward validation to prevent data leakage.

---

## Business Value

RetailScope AI enables:

* Customer retention strategy through churn prediction
* Behavioral segmentation for targeted marketing
* Cross-selling insights through association rules
* Revenue forecasting for operational planning
* Data-driven strategic decision-making

---

<!-- ## Future Improvements

* Model monitoring and drift detection
* MLflow experiment tracking
* Containerization (Docker)
* CI/CD pipeline integration
* GenAI-powered natural language analytics interface

--- -->
