import pandas as pd
import os

def get_paths():
    # Returns paths for silver and gold
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    silver_path = os.path.join(base_path, 'data', 'silver')
    gold_path = os.path.join(base_path, 'data', 'gold')
    return silver_path, gold_path

def process_silver_to_gold():
    silver_path, gold_path = get_paths()
    os.makedirs(gold_path, exist_ok=True)

    # Load silver data
    silver_file = os.path.join(silver_path, 'silver_crypto.parquet')
    if not os.path.exists(silver_file):
        print("Silver file not found. Run process_silver.py first.")
        return
    df_silver = pd.read_parquet(silver_file)

    # Create dim tabble according to the diagram
    crypto_info = [
        {"ticker_key": "BTC/USDT", "full_name": "Bitcoin", "blockchain": "Bitcoin Network", "launch_year": 2009},
        {"ticker_key": "ETH/USDT", "full_name": "Ethereum", "blockchain": "Ethereum Mainnet", "launch_year": 2015},
        {"ticker_key": "SOL/USDT", "full_name": "Solana", "blockchain": "Solana Network", "launch_year": 2020}
    ]
    df_dim = pd.DataFrame(crypto_info)

    # Create fact tabble
    df_fact = df_silver[[
        'datetime', 
        'ticker', 
        'close', 
        'ma_7d', 
        'volume'
    ]].copy()

    # Renaming for better consistency with your ERD
    df_fact.columns = ['date_key', 'ticker_key', 'close_price', 'moving_average_7d', 'volume']

    # Export to Gold 
    dim_output = os.path.join(gold_path, 'dim_crypto.parquet')
    fact_output = os.path.join(gold_path, 'fact_crypto_prices.parquet')

    df_dim.to_parquet(dim_output, index=False)
    df_fact.to_parquet(fact_output, index=False)

    print("\n" + "="*30)
    print("GOLD LAYER COMPLETED")
    print("="*30)
    print(f"Dimension saved: {len(df_dim)} assets")
    print(f"Fact saved: {len(df_fact)} historical records")
    print(f"Location: data/gold/")
    print("="*30)

if __name__ == "__main__":
    process_silver_to_gold()
