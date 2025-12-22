import sqlalchemy
from sqlalchemy import create_engine

# Connection Config
# Format: postgresql+psycopg2://user:password@host:port/dbname
DB_USER = "user"
DB_PASSWORD = "password123"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "crypto_data"

CONNECTION_STRING = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def test_connection():
    try:
        engine = create_engine(CONNECTION_STRING)
        
        # Connect
        with engine.connect() as connection:
            print("✅ Successful Connection!")
            
            # Test Query
            result = connection.execute(sqlalchemy.text("SELECT price, price_eur FROM clean_prices;"))
            print(f"Test Query Result: {result.fetchone()}")
            
    except Exception as e:
        print("❌ Connection Error:")
        print(e)

if __name__ == "__main__":
    test_connection()