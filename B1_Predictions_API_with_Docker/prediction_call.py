import requests
import json

# 1. Config
BASE_URL = "https://news-api-portfolio.onrender.com"
ENDPOINT = "/predict"

full_url = BASE_URL + ENDPOINT

# 2. Payload
# Modify it as you wish
news_to_classify = {
    "text": "Innovation drives modern success. Companies must adapt to rapidly changing markets to survive. Leaders who embrace technology and foster creativity will secure long-term growth and outperform competitors in the global economy."
}

print(f"📡 Calling API: {full_url}...")

try:
    # 3. POST Call
  
    response = requests.post(full_url, json=news_to_classify)

    # 4. Check
    if response.status_code == 200:
        result = response.json()
        print("\n✅ Success!")
        print(f"📝 Input: {result['input_text']}")
        print(f"🏷️  Prediction: {result['predicted_category']}")
    else:
        print(f"\n❌ Error {response.status_code}: {response.text}")

except Exception as e:
    print(f"\n❌ Connection Error: {e}")