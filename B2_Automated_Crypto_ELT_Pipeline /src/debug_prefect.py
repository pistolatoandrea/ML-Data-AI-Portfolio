from dotenv import load_dotenv
import os

load_dotenv()

print(f"🔍 DEBUG: PREFECT_API_URL setted at: {os.getenv('PREFECT_API_URL')}")

from prefect import flow, task
import time

@task
def say_hello():
    print("👋 Hi from Dashboard!")

@flow(name="Diagnostic Test ENV", log_prints=True)
def debug_flow():
    print("🚀 Starting connection test...")
    say_hello()
    time.sleep(2)
    print("✅ Success.")

if __name__ == "__main__":
    debug_flow()