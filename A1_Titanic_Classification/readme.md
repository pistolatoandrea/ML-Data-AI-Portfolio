# Project Titanic Overview🚢

This project analyzes the classic Titanic passenger dataset to build a machine learning model that predicts whether a given passenger survived the 1912 disaster.

**See the full analysis in the notebook:** 

### **👉🏻 [Titanic Jupyter Notebook](./Titanic_Jupyter_Notebook.ipynb)**

The primary goal is to **demonstrate a complete, end-to-end data science workflow,** starting from raw data and finishing with a well-understood, high-performing predictive model and a UI visualization tool.

### **👉🏻 [Interactive Titanic Prediction App](https://pistolatoandrea-ml-data-ai--a1-titanic-classificationapp-1o6gcp.streamlit.app/)**

A live ML-powered app that predicts your odds of surviving the Titanic — trained on real passenger data, deployed on Streamlit Cloud. 

*Please note that the app may take several seconds to wake up on first load.*

## Process & Objectives

This notebook covers the following key steps:

### 1.  Exploratory Data Analysis (EDA):

Using `Seaborn` and `Matplotlib` to visualize the data and uncover key patterns. Variables `Sex`, `Pclass` (Ticket Class), and `Fare` have been identified as strong predictors of survival.

### 2.  Data Cleaning & Preparation:

Loading the dataset and handling missing values (like `Age` and `Embarked`) and transforming non-numeric features (like `Sex`) into machine-readable formats.

### 3.  Model Training & Comparison:

Training four different classification models (`Random Forest`, `Decision Tree`, `Logistic Regression`, and `KNN`) to establish a performance benchmark.

### 4.  Model Evaluation & Analysis:

Comparing the models based on their accuracy scores, and then diving deeper into the best-performing model by analyzing its **Confusion Matrix** and **Feature Importance**.

### 5.  Hyperparameter Tuning:

Using `GridSearchCV` to find the best hyperparameters for the winning model (Random Forest)

## Possible Next Steps

While Random Forest 81% accuracy is a strong result, to overcome this performance plateau, the next logical step would be more advanced **Feature Engineering**.

1.  **Model-Based Age Imputation:** The `age` feature was identified as highly important, yet nearly 20% of its values were missing and imputed using the simple mean. A more accurate approach would be to treat `age` itself as a prediction problem. A regression model (e.g., `RandomForestRegressor`) could be trained on the 714 passengers with known ages—using features like `Pclass` or `parch` to predict the ages for the 177 passengers with missing data. This would provide a more realistic dataset for the final survival model, likely boosting its accuracy.

2.  **Advanced Feature Extraction:**

    * **`Name`**: Extracting titles (e.g., "Mr.", "Mrs.", "Dr.", "Master") could create a new, powerful categorical feature that likely correlates with both age and social status.

    * **`Ticket`**: Analyzing ticket prefixes might reveal correlations to cabin location or booking group, which could also influence survival.
