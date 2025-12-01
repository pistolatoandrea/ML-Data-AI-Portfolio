import streamlit as st
import pickle
import re
import os

# Usiamo le stopwords di Sklearn per evitare errori di download/SSL
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from nltk.stem import PorterStemmer

# 1. Page Configuration
st.set_page_config(page_title="AI News Classifier", page_icon="📰")

# 2. Load Resources (Cached for performance)

@st.cache_resource
def load_resources():

    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Complete Paths for Files

    model_path = os.path.join(current_dir, 'news_classifier_model.pkl')
    vectorizer_path = os.path.join(current_dir, 'tfidf_vectorizer.pkl')
    
    # Load the Model

    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    
    # Load the Vectorizer

    with open(vectorizer_path, 'rb') as file:
        vectorizer = pickle.load(file)
        
    return model, vectorizer

# Initialize resources
# Convert frozenset to set for faster lookups
stop_words = set(ENGLISH_STOP_WORDS) 
stemmer = PorterStemmer()

# 3. Define the Preprocessing Function 
# (Must be identical to training pipeline!)
def preprocess_text(text):
    # Remove non-alphabetic characters
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    # Lowercase
    text = text.lower()
    # Tokenize
    words = text.split()
    # Remove stopwords & Stemming
    clean_words = [stemmer.stem(word) for word in words if word not in stop_words]
    return ' '.join(clean_words)

# 4. Build the UI
st.title("📰 AI News Classifier")
st.markdown("""
This app uses a **Naive Bayes** Machine Learning model to classify news articles into 5 categories:
* 🏢 **Business**
* 🎬 **Entertainment**
* 🗳️ **Politics**
* ⚽ **Sport**
* 💻 **Tech**
""")

# Input Area

st.subheader("Try it yourself")

user_input = st.text_area("Paste a headline or article text here:", height=150, placeholder="Example: Apple releases new iPhone with AI features...")

# Prediction Logic
if st.button("Classify Article", type="primary"):
    if user_input.strip() == "":
        st.warning("Please enter some text first.")
    else:
        try:
            # Load artifacts
            model, vectorizer = load_resources()
            
            # Process input
            cleaned_text = preprocess_text(user_input)
            
            # Vectorize
            vectorized_text = vectorizer.transform([cleaned_text]).toarray()
            
            # Predict
            prediction = model.predict(vectorized_text)[0]
            
            # Probabilities (confidence score)
            probs = model.predict_proba(vectorized_text)[0]
            confidence = max(probs)
            
            # Create columns for layout
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.success(f"### {prediction.upper()}")
                st.metric("Confidence Score", f"{confidence:.1%}")
            
            with col2:
                # Visualization of probabilities
                st.caption("Probability Distribution:")
                st.bar_chart(dict(zip(model.classes_, probs)))
                
        except Exception as e:
            st.error(f"An error occurred: {e}")