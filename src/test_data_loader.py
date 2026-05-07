# Testing
from data_loader import fetch_binance_klines, fetch_fear_greed_index, fetch_blockchain_metric

def test_binance():
    print("Testing Binance fetcher...")
    df = fetch_binance_klines("BTCUSDT", "1d", "2024-01-01")
    assert len(df) > 0, "No data returned!"
    assert "close" in df.columns, "Missing 'close' column!"
    print(f"{len(df)} rows")


def test_fear_greed():
    print("Testing Fear & Greed fetcher...")
    df = fetch_fear_greed_index(limit=30)
    assert len(df) > 0, "No data returned!"
    assert df["fear_greed"].between(0, 100).all(), "Values out of range!"
    print(f"{len(df)} rows")

def test_blockchain_metric():
    print("Testing blockchain.com fetcher...")
    df = fetch_blockchain_metric("hash-rate", timespan="1year")
    assert len(df) > 0, "No data returned!"
    print(f"{len(df)} rows")

if __name__ == "__main__":
    test_binance()
    test_fear_greed()
    test_blockchain_metric()
    print("All tests passed!")