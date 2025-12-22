from dotenv import load_dotenv
load_dotenv()

import requests
import pandas as pd
from datetime import datetime, timedelta
import sqlalchemy
from sqlalchemy import create_engine
from prefect import task, flow

# --- CONFIG ---
COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"
DB_CONNECTION_STRING = "postgresql+psycopg2://user:password123@localhost:5432/crypto_data"

# --- TASKS ---

# --- EXTRACT ---
@task(name="Extract Data", retries=3, retry_delay_seconds=60) 
def extract_data(coin_id="bitcoin", currency="usd"):
    print(f"📡 Extracting data for {coin_id}...")
    params = {"ids": coin_id, "vs_currencies": currency, "include_last_updated_at": "true"}
    
    response = requests.get(COINGECKO_URL, params=params)
    response.raise_for_status()
    
    data = response.json()
    price = data[coin_id][currency]
    timestamp_unix = data[coin_id]['last_updated_at']
    timestamp = datetime.fromtimestamp(timestamp_unix)
    
    df = pd.DataFrame([{
        "coin": coin_id,
        "price": price,
        "currency": currency,
        "timestamp": timestamp,
        "created_at": datetime.now()
    }])
    return df

# --- TRANSFORM ---
@task(name="Transform Data")
def transform_data(df):
    if df is None or df.empty:
        return None
    print("⚙️ Transforming data...")
    USD_TO_EUR_RATE = 0.92 
    df_clean = df.copy()
    df_clean['price_eur'] = df_clean['price'] * USD_TO_EUR_RATE
    df_clean['coin'] = df_clean['coin'].str.upper()
    df_clean['processed_at'] = datetime.now()
    return df_clean

# --- LOAD ---
@task(name="Load Data")
def load_data(df, table_name):
    if df is None:
        return
    print(f"💾 Loading data into table '{table_name}'...")
    engine = create_engine(DB_CONNECTION_STRING)
    df.to_sql(table_name, engine, if_exists="append", index=False)
    print("✅ Data successfully loaded!")

# --- FLOW ---
@flow(name="Crypto ETL Pipeline", log_prints=True)
def crypto_etl_flow():
    # 1. Extract
    df_raw = extract_data("bitcoin")
    
    # 2. Load Raw
    load_data(df_raw, "raw_prices")
    
    # 3. Transform
    df_clean = transform_data(df_raw)
    
    # 4. Load Clean
    load_data(df_clean, "clean_prices")

# --- SCHEDULING ---
if __name__ == "__main__":
    
    print("🕰️ Scheduler Online: Execution every 60 seconds...")
    
    crypto_etl_flow.serve(
        name="my-local-deployment",
        interval=600, # 600 seconds
        tags=["dev", "crypto"],
        description="Pipeline that downloads Bitcoin every minute."
    )