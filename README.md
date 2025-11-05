# 🚢 Titanic ML Project

### 🚀 **View the Live Interactive Demo https://titanic-ml-project.streamlit.app/**

This project is an end-to-end data science analysis that predicts passenger survival from the Titanic disaster.

All detailed analysis, exploratory data analysis (EDA), and model comparison are located within the main Jupyter Notebook 

The notebook covers the following key steps:

1.  **Exploratory Data Analysis (EDA):** Using `Seaborn` and `Matplotlib` to visualize the data and uncover key patterns. `Sex`, `Pclass` (Ticket Class), and `Fare` are identified as strong predictors of survival.
2.  **Data Cleaning & Preparation:** Loading the dataset and handling missing values (like `Age` and `Embarked`) and transforming non-numeric features (like `Sex`) into machine-readable formats.
3.  **Model Training & Comparison:** Training four different classification models (`Random Forest`, `Decision Tree`, `Logistic Regression`, and `KNN`) to establish a performance benchmark.
4.  **Model Evaluation & Analysis:** Comparing the models based on their accuracy scores, and then diving deeper into the best-performing model (Random Forest) by analyzing its **Confusion Matrix** and **Feature Importance**.

### Project Quick View

* **Full Analysis Jupyter Notebook:** `Titanic_ML_Project.ipynb'
* **Interactive App Code:** `app_titanic.py`
* **App Libraries** 'requirements.txt'
* **Model:** 'titanic_model.pkl'
  
### Tech Stack

* Jupyter Notebook (for analysis, experimentation and process documentation)
* Python
* Pandas (for data cleaning and manipulation)
* Scikit-learn (for model training and evaluation)
* Streamlit (for the interactive demo)
* Joblib (for saving the trained model)

### Deployment Process

The interactive demo is hosted on **Streamlit Cloud**. The process was:

1.  **Model Export:** The final, tuned Random Forest model (`.pkl`) was saved from the notebook.
2.  **App Creation:** An `app_titanic.py` script was built to load the model and generate a UI with `Streamlit`.
3.  **GitHub Push:** The app (`app_titanic.py`), the model (`.pkl`), and dependencies (`requirements.txt`) were pushed to this repository.
4.  **Deploy:** The repository was linked to Streamlit Cloud, which automatically built and published the app at the link above.
