import ccxt 
import json
import os
from datetime import datetime
import time

# List of assets we will use
COIN_LIST = ["BTC/USDT", "ETH/USDT", "SOL/USDT"]
TIMEFRAME = '1d' # Daily data
LIMIT = 500      # Last 500 days

exchange = ccxt.binance({
    'enableRateLimit' : True
})

def get_bronze_path():
    # returns the path to data/bronze
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    bronze_path = os.path.join(base_path, 'data', 'bronze')
    return bronze_path

def search_and_save_bronze():
    # Function to seach raw data and save Json
    save_path = get_bronze_path()

    os.makedirs(save_path, exist_ok=True)
    for coin in COIN_LIST:
        print(f"Starting ingestion of {coin}..")

        try:
            # Request OHLCV data from API
            raw_data = exchange.fetch_ohlcv(coin, timeframe=TIMEFRAME, limit=LIMIT)
            
            # Structure the data 
            # Format: [timestamp, open, high, low, close, volume]
            formatted_data = {
                "ticker": coin,
                "extraction_at": datetime.now().isoformat(),
                "timeframe": TIMEFRAME,
                "prices": [
                    {
                        "timestamp": item[0],
                        "open": item[1],
                        "high": item[2],
                        "low": item[3],
                        "close": item[4],
                        "volume": item[5]
                    } for item in raw_data
                ]
            }
            
            # Define filename and save to JSON
            file_name = f"raw_{coin.replace('/', '_')}.json"
            full_path = os.path.join(save_path, file_name)
            
            with open(full_path, 'w') as f:
                json.dump(formatted_data, f, indent=4)
            
            print(f"Success! Data saved to {file_name}")
            
            # Small pause for stability
            time.sleep(1)

        except Exception as e:
            # Error handling to keep the loop running if one coin fails
            print(f"Error searching{coin}: {e}")

if __name__ == "__main__":
    search_and_save_bronze()