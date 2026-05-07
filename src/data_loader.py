import requests
import pandas as pd
import time

# FETCH BINANCE 
def fetch_binance_klines(symbol="BTCUSDT", interval="1d", start_date="2020-01-01", end_date=None):
    """
    Fetch OHLCV data from Binance public API.
    
    Args:
        symbol: Trading pair (e.g., 'BTCUSDT', 'ETHUSDT')
        interval: '1m', '5m', '1h', '4h', '1d', '1w'
        start_date: 'YYYY-MM-DD'
        end_date: 'YYYY-MM-DD' (defaults to today)
    
    Returns:
        DataFrame with columns: date, open, high, low, close, volume
    """
     
    url = "https://api.binance.com/api/v3/klines"
    
    # Convert dates to milliseconds 
    start_ms = int(pd.Timestamp(start_date).timestamp() * 1000)
    if end_date is None:
        end_ms = int(pd.Timestamp.now().timestamp() * 1000)
    else:
        end_ms = int(pd.Timestamp(end_date).timestamp() * 1000)
    
    all_data = []
    current_start = start_ms
    
    # Binance returns max 1000 candles per call
    while current_start < end_ms:
        params = {
            "symbol": symbol,
            "interval": interval,
            "startTime": current_start,
            "endTime": end_ms,
            "limit": 1000
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise error if request failed
        data = response.json()
        
        if not data:
            break
        
        all_data.extend(data)
        # Move start to last candle's close time + 1ms
        current_start = data[-1][6] + 1
        
        time.sleep(0.2)
    
    # Convert to DataFrame
    columns = [
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_volume", "trades", 
        "taker_buy_base", "taker_buy_quote", "ignore"
    ]
    df = pd.DataFrame(all_data, columns=columns)
    
    # Keep only what we need
    df["date"] = pd.to_datetime(df["open_time"], unit="ms").dt.date
    df = df[["date", "open", "high", "low", "close", "volume"]]
    
    # Convert string numbers to float
    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = df[col].astype(float)
    
    df["date"] = pd.to_datetime(df["date"])
    df = df.drop_duplicates(subset="date").reset_index(drop=True)
    
    return df

# FETCH FEAR AND GREED
def fetch_fear_greed_index(limit=0):
    """
    Fetch the Crypto Fear & Greed Index from alternative.me.
    
    Args:
        limit: Number of days to fetch. 0 = all available data.
    
    Returns:
        DataFrame with columns: date, fear_greed, fear_greed_label
    """
    url = "https://api.alternative.me/fng/"
    params = {"limit": limit}  
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    
    # Extract the list of daily readings
    records = data["data"]
    
    df = pd.DataFrame(records)
    
    # Clean up columns
    df["date"] = pd.to_datetime(df["timestamp"].astype(int), unit="s")
    df["fear_greed"] = df["value"].astype(int)
    df["fear_greed_label"] = df["value_classification"]
    
    df = df[["date", "fear_greed", "fear_greed_label"]]
    
    # Sort oldest to newest (API returns newest first)
    df = df.sort_values("date").reset_index(drop=True)
    
    return df

# FETCH BLOCKCHAIN
def fetch_blockchain_metric(metric="hash-rate", timespan="all"):
    """
    Fetch on-chain Bitcoin metrics from blockchain.com.
    
    Args:
        metric: One of:
            'hash-rate'         — mining power
            'n-transactions'    — daily transaction count
            'mempool-size'      — unconfirmed transactions
            'avg-block-size'    — average block size
            'difficulty'        — mining difficulty
        timespan: 'all', '5years', '2years', '1year'
    
    Returns:
        DataFrame with columns: date, <metric>
    """
    url = f"https://api.blockchain.info/charts/{metric}"
    params = {
        "timespan": timespan,
        "format": "json",
        "sampled": "false"  # raw daily data, not sampled
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    
    # 'values' is a list of {x: timestamp, y: value} dicts
    records = data["values"]
    
    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["x"], unit="s")
    df = df.rename(columns={"y": metric.replace("-", "_")})
    df = df[["date", metric.replace("-", "_")]]
    
    # Normalize date (drop time portion) for clean merging
    df["date"] = df["date"].dt.normalize()
    
    return df

# MERGE
def merge_all_sources(btc_path, fg_path, onchain_path, start_date="2020-01-01"):
    """
    Merge all data sources into a single master DataFrame aligned on date.
    
    Args:
        btc_path: Path to BTC prices CSV
        fg_path: Path to Fear & Greed CSV
        onchain_path: Path to on-chain metrics CSV
        start_date: Earliest date to keep
    
    Returns:
        Merged DataFrame, sorted by date, with NaN handling
    """
    # Load all CSVs
    btc = pd.read_csv(btc_path, parse_dates=["date"])
    fg = pd.read_csv(fg_path, parse_dates=["date"])
    onchain = pd.read_csv(onchain_path, parse_dates=["date"])
    
    # Drop the text label from F&G (we'll keep numeric only for ML)
    if "fear_greed_label" in fg.columns:
        fg = fg.drop(columns=["fear_greed_label"])
    
    # Start with BTC as the "spine" (it's our prediction target)
    df = btc.copy()
    
    # Left join keeps every BTC row, fills with NaN if other sources are missing
    df = df.merge(fg, on="date", how="left")
    df = df.merge(onchain, on="date", how="left")
    
    # Filter to our date range
    df = df[df["date"] >= pd.Timestamp(start_date)].reset_index(drop=True)
    
    # Sort by date (just in case)
    df = df.sort_values("date").reset_index(drop=True)
    
    return df