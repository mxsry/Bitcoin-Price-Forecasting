# Bitcoin Price Forecasting

End-to-end time series forecasting project predicting Bitcoin price using multiple data sources: market data, sentiment, and on-chain metrics.

## 🎯 Project Goals

- Build a reproducible data pipeline pulling from real APIs
- Compare classical, machine learning, and deep learning forecasting methods
- Honestly evaluate models with walk-forward validation
- Deploy results in an interactive dashboard

## 📊 Data Sources

| Source | Data | API |
|--------|------|-----|
| Binance | BTC/USDT OHLCV daily prices | `api.binance.com` |
| alternative.me | Crypto Fear & Greed Index | `api.alternative.me` |
| blockchain.com | Hash rate, transaction count | `api.blockchain.info` |

## 🛠️ Tech Stack

- **Data:** pandas, requests
- **Machine Learning:** scikit-learn, XGBoost, LightGBM
- **Deep Learning:** TensorFlow / Keras
- **Stats:** statsmodels (ARIMA)
- **Visuallize:** matplotlib, seaborn, plotly
- **Dashboard:** Streamlit

## 📁 Project Structure
```
bitcoin-price-forecasting/
│
├── data/
│   ├── raw/                  # Raw API / exchange data
│   └── processed/            # Cleaned, transformed datasets
│
├── notebooks/                # Jupyter notebooks for EDA & experiments
│
├── src/                      # Source code modules
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   ├── train.py
│   └── evaluate.py
│
├── models/                   # Saved trained models
│   ├── lstm_model.pkl
│   └── xgboost_model.pkl
│
├── reports/                  # Generated reports, plots, metrics
│   ├── figures/
│   └── results.md
│
├── app/                      # Streamlit dashboard app
│   ├── app.py
│   └── components/
│
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── .gitignore
└── LICENSE
```