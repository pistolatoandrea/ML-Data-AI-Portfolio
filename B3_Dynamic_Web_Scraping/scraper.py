import os
import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURAZIONE ---
BASE_URL = "https://quotes.toscrape.com/js/"
RAW_DATA_PATH = "data/raw"
CLEAN_DATA_PATH = "data/clean"

def setup_driver():
    """Chrome Config & Anonymization"""
    chrome_options = Options()
    
    # 1. HEADLESS for no interface (comment to remove)
    chrome_options.add_argument("--headless") 
    
    # 2. USER-AGENT
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    chrome_options.add_argument(f"user-agent={user_agent}")
    
    # 3. Other Options to avoid common issues in Docker/Linux environment
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def clean_text(text):
    """Cleaning and pre-processing"""
    
    if text:
        return text.replace('“', '').replace('”', '').strip()
    return text

def save_data(data_list):
    """Save Data in a Data Lake Structure"""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
  
    os.makedirs(RAW_DATA_PATH, exist_ok=True)
    os.makedirs(CLEAN_DATA_PATH, exist_ok=True)
    
    df = pd.DataFrame(data_list)
    
    # 1. BRONZE LAYER (RAW)
    raw_filename = f"{RAW_DATA_PATH}/quotes_raw_{timestamp}.json"
    df.to_json(raw_filename, orient='records', indent=4)
    print(f"✅ Raw Data saved in: {raw_filename}")
    
    # 2. SILVER LAYER (CLEAN):
    df_clean = df.copy()
   
    df_clean['text'] = df_clean['text'].apply(clean_text)
  
    df_clean = df_clean.drop(columns=['page'])
    
    clean_filename = f"{CLEAN_DATA_PATH}/quotes_clean_{timestamp}.csv"
    df_clean.to_csv(clean_filename, index=False)
    print(f"✅ Clean Data saved in: {clean_filename}")

# --- MAIN ---
def main():
    driver = setup_driver()
    all_quotes = []
    page_number = 1
    
    print("🚀 Start Scraping...")
    
    try:
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 10)
        
        while True:
            print(f"Scraping page {page_number}...")
            
            # Wait and Gather Quotes per Page
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "quote")))
            cards = driver.find_elements(By.CLASS_NAME, "quote")
            
            for card in cards:
                try:
                    text = card.find_element(By.CLASS_NAME, "text").text
                    author = card.find_element(By.CLASS_NAME, "author").text
                    all_quotes.append({
                        "text": text, 
                        "author": author, 
                        "page": page_number
                    })
                except Exception as e:
                    print(f"Errore su una card: {e}")

            # Next Page
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, "li.next > a")
                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(1.5)
                page_number += 1
            except:
                print("End of Available Pages")
                break
                
    except Exception as e:
        print(f"Critical Error: {e}")
    finally:
        driver.quit()
        
    # Save
    if all_quotes:
        save_data(all_quotes)
    else:
        print("⚠️ No Data")

if __name__ == "__main__":
    main()