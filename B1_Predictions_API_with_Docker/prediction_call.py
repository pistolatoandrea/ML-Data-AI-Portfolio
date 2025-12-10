import requests
import json

# 1. Config
BASE_URL = "https://news-api-portfolio.onrender.com"
ENDPOINT = "/predict"

full_url = BASE_URL + ENDPOINT

# 2. Payload
# Modify it as you wish
news_to_classify = {
    "text": "Rockets Soar with Last-Second Stunner. In a stunning buzzer-beater finish, the Houston Rockets edged out the Chicago Bulls 98-96 last night. Trailing by ten in the fourth quarter, rookie Jalen Green sank a fading three-pointer as time expired, sending the home crowd into a frenzy. This victory marks their fifth consecutive win this season"
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