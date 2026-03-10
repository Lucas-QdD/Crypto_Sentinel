import pandas as pd
import os
import json
from datetime import datetime

# 7-day moving average window
MA_WINDOW = 7

def get_paths():
    # Returns paths for bronze (input) and silver (output)
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    bronze_path = os.path.join(base_path, 'data', 'bronze')
    silver_path = os.path.join(base_path, 'data', 'silver')
    return bronze_path, silver_path

def process_bronze_to_silver():
    bronze_path, silver_path = get_paths()
    os.makedirs(silver_path, exist_ok=True)
    
    all_dfs = [] # List to store dataframes of each coin
    
    # Scanning and Reading Bronze Files 
    print("Scanning Bronze layer")
    files = [f for f in os.listdir(bronze_path) if f.endswith('.json')]
    
    if not files:
        print("No JSON files found in Bronze folder.")
        return

    for file in files:
        file_path = os.path.join(bronze_path, file)
        
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        # Convert the 'prices' list into a DataFrame 
        df = pd.DataFrame(data['prices'])
        df['ticker'] = data['ticker'] # Identify the coin 
        all_dfs.append(df)
        print(f"Read: {data['ticker']} ({len(df)} rows)")

    # Merge
    # Stack all dataframes together | Empilha todos os dataframes
    master_df = pd.concat(all_dfs, ignore_index=True)

    # Data Transformation
    # Convert Timestamp (ms) to Readable Date 
    master_df['datetime'] = pd.to_datetime(master_df['timestamp'], unit='ms')
    
    # Sort by ticker and date for correct MA calculation 
    master_df = master_df.sort_values(by=['ticker', 'datetime'])

    #Feature Engineering: Moving Average 
    # We group by ticker so the MA doesn't mix data from different coins
    master_df[f'ma_{MA_WINDOW}d'] = master_df.groupby('ticker')['close'].transform(
        lambda x: x.rolling(window=MA_WINDOW).mean()
    )

    # Export to Parquet (Overwrite each time it runs)
    output_file = os.path.join(silver_path, 'silver_crypto.parquet')
    master_df.to_parquet(output_file, index=False)

    # terminal summary
    print("\n" + "-"*30)
    print("SILVER PROCESSING SUMMARY")
    print("-"*30)
    summary = master_df.groupby('ticker').size()
    for ticker, count in summary.items():
        print(f"🔹 {ticker}: {count} records processed")
    print(f"\nfile saved at: data/silver/silver_crypto.parquet")
    print(f"Total rows: {len(master_df)}")
    print("="*30)

if __name__ == "__main__":
    process_bronze_to_silver()