# Bitcoin Price Forecasting Using Real-time Datasets

End-to-end time series forecasting project predicting Bitcoin price using multiple data sources included market data, sentiment, and on-chain metrics.

## 🎯 Project Goals

- Build a reproducible data pipeline pulling from real APIs
- Visuallize data, explore data analysis
- Compare classical, machine learning, and deep learning forecasting methods

## 📊 Data Sources

| Source | Data | API |
|--------|------|-----|
| Binance | BTC/USDT OHLCV daily prices | `api.binance.com` |
| alternative.me | Crypto Fear & Greed Index | `api.alternative.me` |
| blockchain.com | Hash rate, transaction count | `api.blockchain.info` |

## 🛠️ Tech Stack

- **Data Handling:** pandas, requests, numpy
- **Machine Learning:** scikit-learn, XGBoost
- **Visuallize:** matplotlib, seaborn, plotly

## 📁 Project Structure
```
bitcoin-price-forecasting/
├── data/
│   ├── raw/              # Raw API dataset
│   └── processed/        # Cleaned & merged dataset
├── notebooks/            
│   ├── data_collection.ipynb   
│   ├── eda.ipynb             
│   ├── feature_engineering.ipynb  
│   └── modeling.ipynb         
├── src/                  
│   ├── data_loader.py
│   └── test_data_loader.py
├── requirements.txt           
└── README.md
```