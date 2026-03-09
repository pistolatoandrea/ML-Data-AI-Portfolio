from dotenv import load_dotenv
load_dotenv()

import requests
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from prefect import task, flow

# --- CONFIG ---
COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"
# In produzione useremmo variabili d'ambiente, ma per ora va bene così
DB_CONNECTION_STRING = "postgresql+psycopg2://user:password123@localhost:5432/crypto_data"

# --- TASKS ---

@task(name="Extract Data", retries=3, retry_delay_seconds=60) 
def extract_data(coin_id="bitcoin", currency="usd"):
    print(f"📡 Extracting raw data for {coin_id}...")
    params = {
        "ids": coin_id, 
        "vs_currencies": currency, 
        "include_last_updated_at": "true"
    }
    
    try:
        response = requests.get(COINGECKO_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        # ELT: Prendiamo i dati grezzi. 
        # Non convertiamo in EUR qui. Lasciamo che lo faccia dbt.
        price = data[coin_id][currency]
        timestamp_unix = data[coin_id]['last_updated_at']
        timestamp = datetime.fromtimestamp(timestamp_unix)
        
        # Creiamo un DataFrame che rispecchia il dato grezzo
        df = pd.DataFrame([{
            "coin_id": coin_id,
            "vs_currency": currency,
            "price": price,
            "last_updated": timestamp,
            "extracted_at": datetime.now()
        }])
        return df

    except Exception as e:
        print(f"❌ Error extracting data: {e}")
        raise e

@task(name="Load Raw Data")
def load_data(df, table_name):
    if df is None or df.empty:
        print("⚠️ No data to load.")
        return
        
    print(f"💾 Loading raw data into '{table_name}'...")
    engine = create_engine(DB_CONNECTION_STRING)
    
    # ELT Best Practice: 'append'.
    # Creiamo uno storico completo (Log) di tutto ciò che arriva.
    with engine.connect() as conn:
        df.to_sql(table_name, engine, if_exists="append", index=False)
        
    print("✅ Raw data loaded successfully!")

# --- FLOW ---
@flow(name="Crypto ELT - Raw Ingestion", log_prints=True)
def crypto_elt_flow():
    # 1. Extract
    df_raw = extract_data("bitcoin", "usd")
    
    # 2. Load Raw
    load_data(df_raw, "raw_bitcoin")

# --- SCHEDULING ---
if __name__ == "__main__":
    print("🕰️ Scheduler Online: Ingestion every 5 minutes...")
    
    # IMPORTANTE: Ho cambiato il nome del deployment in "ingest-raw-v1".
    # Questo serve a far dimenticare a Prefect il vecchio storico ed evitare errori.
    crypto_elt_flow.serve(
        name="ingest-raw-v1", 
        interval=300, # 5 minuti
        tags=["elt", "raw"],
        description="Ingestion pura di dati raw da CoinGecko."
    )