import streamlit as st
import pandas as pd
import joblib

# Load Model Function
@st.cache_resource
def load_model():
    model = joblib.load('titanic_model.pkl')
    return model

model = load_model()

# App Title and Description
st.title('Titanic Survival Predictor 🚢')
st.write('This app predicts whether a passenger would have survived the Titanic disaster.')

# User Inputs

st.header('Insert passenger details:')

col1, col2, col3 = st.columns(3) # 3 columns for improved readability

with col1:
    pclass = st.selectbox('Passenger Ticket Class', [1, 2, 3])
    sex = st.selectbox('Sex', ['male', 'female'])

with col2:
    age = st.slider('Age', 0, 80, 29) # min, max, default
    sibsp = st.number_input('Number of siblings and spouses', 0, 8, 0) # min, max, default

with col3:
    parch = st.number_input('Number of parents and children', 0, 6, 0)
    fare = st.number_input('Ticket Fare ($)', 0.0, 512.0, 32.0, format="%.2f")

embarked = st.selectbox('Port of Departure', ['Southampton', 'Cherbourg', 'Queenstown'])

# Forecast Button
if st.button('Predict survival'):
    
    # Input Preprocessing
    
    # 1. Sex
    sex_numeric = 1 if sex == 'female' else 0
    
    # 2. Port of Departure (One-Hot Encoding with dummy variables)
    # Default value is 'Cherbourg'

    embarked_Q = 1 if embarked == 'Queenstown' else 0
    embarked_S = 1 if embarked == 'Southampton' else 0
    
    # 3. Alone Feature

    alone = 1 if (sibsp + parch) == 0 else 0
    
    # Prediction DataFrame

    feature_names = ['pclass', 'sex', 'age', 'sibsp', 'parch', 'fare', 'alone', 'embarked_Q', 'embarked_S']
    
    features_df = pd.DataFrame([[
        pclass, 
        sex_numeric, 
        age, 
        sibsp, 
        parch, 
        fare, 
        alone, 
        embarked_Q, 
        embarked_S
    ]], columns=feature_names)
    
    # Prediction Execution
    prediction = model.predict(features_df)
    probability = model.predict_proba(features_df)[0]

    # Print Results
    if prediction[0] == 1:
        st.success('**Result: SURVIVED** 🎉')
        st.write(f"Survival Probability: {probability[1]*100:.2f}%")
    else:
        st.error('**Result: NON SURVIVED** 😢')
        st.write(f"Survival Probability: {probability[0]*100:.2f}%")