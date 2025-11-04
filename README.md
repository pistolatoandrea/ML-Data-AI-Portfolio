# Project Titanic🚢

This project analyzes the classic Titanic passenger dataset to build a machine learning model that predicts whether a given passenger survived the 1912 disaster.

**See the full analysis in the notebook:** [Titanic_ML_Project.ipynb]

## Project Overview

This project analyzes the classic *Titanic passenger dataset* to build a machine learning model that predicts whether a given passenger survived the 1912 disaster.

The primary goal is to **demonstrate a complete, end-to-end data science workflow,** starting from raw data and finishing with a well-understood, high-performing predictive model.

### Process & Objectives

This notebook covers the following key steps:

1.  **Exploratory Data Analysis (EDA):** Using `Seaborn` and `Matplotlib` to visualize the data and uncover key patterns. We identified `Sex`, `Pclass` (Ticket Class), and `Fare` as strong predictors of survival.
2.  **Data Cleaning & Preparation:** Loading the dataset and handling missing values (like `Age` and `Embarked`) and transforming non-numeric features (like `Sex`) into machine-readable formats.
3.  **Model Training & Comparison:** Training four different classification models (`Random Forest`, `Decision Tree`, `Logistic Regression`, and `KNN`) to establish a performance benchmark.
4.  **Model Evaluation & Analysis:** Comparing the models based on their accuracy scores, and then diving deeper into the best-performing model (Random Forest) by analyzing its **Confusion Matrix** and **Feature Importance**.

## 1. Exploratory Data Analysis (EDA)📁

In this section, the goal is to explore the dataset, without considering missing values, visually to understand its structure, find patterns, and identify which features (columns) might be good predictors for survival. This is done by plotting the relationships between different variables and the `survived` target column.

### Analytical Approach

* First, **categorical features** (like `Sex` or `Pclass`) are analyzed using **bar charts** (`sns.countplot`). These plots are ideal for comparing survival counts (survived vs. not survived) across different discrete groups.
* Second, **continuous features** (like `Age` or `Fare`) are examined using **density plots** (`sns.kdeplot`). These plots help visualize the distribution of values and compare the shape of the data for survivors versus non-survivors.

### Key findings from this analysis:

* **`Sex`:** This was the strongest predictor. Females had a much higher survival rate than males.
* **`Pclass`:** Ticket class was a clear indicator. Passengers in 1st Class had a significantly higher chance of survival than those in 3rd Class.
* **`Age` & `Fare`:** These numeric features also showed important trends. A large peak in survival was observed for young children (`Age`), and a higher `Fare` generally correlated with a better survival chance.

## 2. Data Cleaning & Preparation 🧹

This section prepares the dataset for modeling. All non-numeric data (text strings) and missing values (NaN) must be handled and converted into a numeric format that the machine learning models can understand.

The following steps are performed:

1.  **Create Backup:** A copy of the original DataFrame is saved before applying transformations.
2.  **Impute 'Age'**: Missing `Age` values (NaN) are filled using the dataset's mean age.
3.  **Drop 'Deck' Column**: The `Deck` column is removed entirely, as it contains too many missing values to be useful.
4.  **Impute 'Embarked'**: The few missing `Embarked` values are filled using the column's mode (the most frequent port of embarkation).
5.  **Drop Unnecessary Columns**: Columns that are redundant (e.g., `embark_town`) or unhelpful for the model (e.g., `PassengerId`, `Name`, `Ticket`) are dropped.
6.  **Encode 'Sex'**: The categorical `Sex` column is converted into a binary numeric format (e.g., `male=0`, `female=1`).
7.  **Encode 'Embarked'**: The categorical `Embarked` column is converted into numerical dummy variables using one-hot encoding.

# 3. Model Training & Comparison 🚀

With a clean, numeric dataset, the next step is to train and evaluate different machine learning models to find the best-performing one.

### Splitting the Data

First, the dataset is split into two separate parts:
* A **Training Set** (used to teach the models).
* A **Testing Set** (held back to evaluate the models on unseen data).

### Model Benchmarking

Four different classification models were trained on the training set and then evaluated against the testing set:

1. **Decision Tree**
2. **Random Forest**
3. **Logistic Regression**
4. **K-Nearest Neighbors (KNN)**

The **Accuracy Score** (the percentage of correct predictions) was used as the primary metric to compare their performance. This "benchmark" process helps identify which model algorithm is most effective for this specific dataset.

# 4. Model Evaluation & Analysis 📈

After the initial benchmark, the **Random Forest** was identified as the top-performing model. This section dives deeper into its performance, moving beyond simple accuracy to understand *how* and *why* it works.

Three key analyses were performed on the winning model:

* **Confusion Matrix:** A heatmap was generated to visualize the model's performance. This shows the exact breakdown of its predictions, detailing the counts of True Positives, True Negatives, False Positives, and False Negatives, which helps in understanding the *types* of errors being made.
* **Feature Importance:** The model was analyzed to determine which features (columns) had the most impact on its decisions. This confirmed that `sex`, `fare`, and `age` were the most significant predictors.
* **Hyperparameter Tuning:** Finally, `GridSearchCV` was used to search for a more optimal set of parameters for the Random Forest. This process confirmed that the default settings were already highly effective and close to the optimal configuration for this dataset.

# Conclusion & Final Results

This project followed the **complete data science lifecycle**: from initial data cleaning to predictive model optimization.

### Key Findings

Four different classification models were benchmarked to determine which was best suited for predicting passenger survival. The final performance ranking on the **test set** is as follows:

1.  **Random Forest:** 81.01% (The winning model)
2.  **Logistic Regression:** 79.33%
3.  **Decision Tree:** 77.09%
4.  **KNN (Best):** 72.07%

### Analysis of the Winning Model (Random Forest)

The focus was placed on the **Random Forest** for a deeper analysis:

* **Feature Importance:** The model's analysis confirmed the findings from the Exploratory Data Analysis (EDA). The three most important features the model used to make its decisions were, in order:
    1.  `sex`
    2.  `fare`
    3.  `age`

* **Hyperparameter Tuning:** `GridSearchCV` was used to find the best hyperparameters. It was discovered that the model's default settings were already near-optimal, as the accuracy on the test set remained unchanged (81.01%). This indicates that the Scikit-learn default model is very robust and that the maximum potential achievable *with the current features* has likely been reached.

### Possible Next Steps

While 81% is a strong result, to overcome this performance plateau, the next logical step would be more advanced **Feature Engineering**.

1.  **Model-Based Age Imputation:** The `age` feature was identified as highly important, yet nearly 20% of its values were missing and imputed using the simple mean. A more accurate approach would be to treat `age` itself as a prediction problem. A regression model (e.g., `RandomForestRegressor`) could be trained on the 714 passengers with known ages—using features like `Pclass` or `parch` to predict the ages for the 177 passengers with missing data. This would provide a more realistic dataset for the final survival model, likely boosting its accuracy.

2.  **Advanced Feature Extraction:**
    * **`Name`**: Extracting titles (e.g., "Mr.", "Mrs.", "Dr.", "Master") could create a new, powerful categorical feature that likely correlates with both age and social status.
    * **`Ticket`**: Analyzing ticket prefixes might reveal correlations to cabin location or booking group, which could also influence survival.
