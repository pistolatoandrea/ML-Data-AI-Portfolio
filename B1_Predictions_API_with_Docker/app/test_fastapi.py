import os
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# 1. Initialize the App

app = FastAPI(
    title="News Classifier API",
    version="1.0",
    description="A simple API to classify news articles using a pre-trained ML model."
)

# 2. Define the Input Schema using Pydantic
# This acts as a contract: the API will only accept data that matches this structure.

class NewsRequest(BaseModel):
    text: str

# 3. Load the Model at Startup
# We use a relative path to locate the .pkl file.

model_path = "app/model/news_classifier.pkl"

if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at: {model_path}")

print(f"Loading model from {model_path}...")
model = joblib.load(model_path)

# 4. Define the Root Endpoint

@app.get("/")
def read_root():
    return {"status": "active", "message": "News Classifier API is ready for predictions!"}

# 5. Define the Prediction Endpoint
# We use POST because we are sending data (the news text) to the server.

@app.post("/predict")
def predict_news(request: NewsRequest):
    """
    Receives a news text and returns the predicted category.
    """
    try:
        # Extract text from the request object
        input_text = request.text
        
        # Make prediction (expecting the model to handle raw text via a Pipeline)
        # We wrap input_text in a list because sklearn expects an iterable usually
        prediction = model.predict([input_text])[0]
        
        # Return the result as JSON
        return {
            "input_text": input_text,
            "predicted_category": str(prediction)
        }
    except Exception as e:
        # If something goes wrong, return a 500 error with details
        raise HTTPException(status_code=500, detail=str(e))