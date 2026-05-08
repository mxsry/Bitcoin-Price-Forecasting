# Bitcoin Price Forecasting

End-to-end time series forecasting project predicting Bitcoin price using multiple data sources: market data, sentiment, and on-chain metrics.

## 🎯 Project Goals

- Build a reproducible data pipeline pulling from real APIs
- Compare classical, machine learning, and deep learning forecasting methods
- Evaluate models with walk-forward validation
- Deploy results in an interactive dashboard

## 📊 Data Sources

| Source | Data | API |
|--------|------|-----|
| Binance | BTC/USDT OHLCV daily prices | `api.binance.com` |
| alternative.me | Crypto Fear & Greed Index | `api.alternative.me` |
| blockchain.com | Hash rate, transaction count | `api.blockchain.info` |

## 🛠️ Tech Stack

- **Data Handling:** pandas, requests, numpy
- **Machine Learning:** scikit-learn, XGBoost, LightGBM
- **Deep Learning:** TensorFlow / Keras
- **Stats:** statsmodels (ARIMA)
- **Visuallize:** matplotlib, seaborn, plotly
- **Dashboard:** Streamlit

## 📁 Project Structure
```
bitcoin-price-forecasting/
├── data/
│   ├── raw/              # Raw API data
│   └── processed/        # Cleaned & merged
├── notebooks/            # Jupyter analysis
├── src/                  # Reusable modules
├── models/               # Trained models
├── reports/              # Figures & results
└── app/                  # Streamlit dashboard
```