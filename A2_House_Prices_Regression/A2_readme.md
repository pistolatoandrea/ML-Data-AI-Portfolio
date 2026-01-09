# 🏠 House Prices Project

This project builds an end-to-end **regression model** to predict a continuous numerical value—the **final sale price** of residential properties—using the complex **Ames Housing dataset**.

The primary goal is to **demonstrate a complete, end-to-end data science workflow,** starting from raw data and finishing with a highly accurate and interpretable predictive model.

**See the full analysis in the notebook:** 

[House\_Prices.ipynb](./House_Prices.ipynb)


## Project Overview

### Process & Objectives

This notebook covers the following key steps:

1.  **Exploratory Data Analysis (EDA):** Analyzing the distribution of the target variable (`SalePrice`) and its correlation with key features.
2.  **Feature Engineering & Data Preparation:** Cleaning the data by imputing missing values, encoding categorical features, scaling numerical data, and creating high-impact new features (e.g., `TotalSqFt`, `HouseAge`, `TotalBath`).
3.  **Modeling & Comparison:** Training a variety of regression models (**Linear Regression**, **Lasso**, **Random Forest**, and **XGBoost**) to benchmark performance.
4.  **Evaluation & Feature Importance Analysis:** Measuring model performance using **RMSE** (Root Mean Squared Error) and **$R^2$** (R-squared), and then analyzing the winning model to determine the most influential predictors of price.

***

## 1. Exploratory Data Analysis (EDA) & Target Transformation 📈

The initial analysis revealed a **right-skewed distribution** for the target variable, `SalePrice`, which is common in financial data.

### Key EDA Steps

* **Target Analysis:** The `SalePrice` distribution was highly asymmetrical.
    * To satisfy the assumptions of linear models and stabilize the variance, a **Log Transformation (`np.log1p`)** was applied to the target to create a more **symmetrical, bell-shaped distribution** (Normalization). This transformation prevents high-value outliers from disproportionately influencing the regression coefficients.
* **Missing Data Audit:** A detailed audit identified features with significant missing values (e.g., `PoolQC` at 99.65%, `Alley` at 93.48%). This step was critical for planning the imputation strategy, as many missing values actually signify the **absence of a feature** (e.g., a missing value in `PoolQC` likely means "No Pool").

***

## 2. Data Cleaning & Feature Engineering 🧹

This phase prepared the high-dimensional, mixed-type dataset for machine learning by aggressively cleaning and transforming features.

### Missing Data Management

Missing values were handled based on domain-specific logic:
* **Dropped Columns:** Irrelevant or overwhelmingly empty columns were removed (`PID`, `MiscFeature`, `Prop_Addr`, `GeoRefNo`).
* **Imputation with "None":** Categorical features where `NaN` indicated "not present" (like `Alley`, `PoolQC`, `FireplaceQu`, and various Basement/Garage features) were imputed with the string **"None"**.
* **Imputation with Zero (0):** Numerical features associated with an absence (like `MasVnrArea`, `GarageArea`, and `TotalBsmtSF`) were imputed with **0**.
* **Statistical Imputation:** The few remaining missing values were handled statistically. `Electrical` was filled with the **mode**, and `LotFrontage`, `Latitude`, and `Longitude` were filled using the **median** grouped by `Neighborhood` for local accuracy.

### High-Impact Feature Creation

Three composite features were engineered to provide the model with better predictive power:
* **`TotalSqFt`:** Sum of ground living area and total basement area (`GrLivArea` + `TotalBsmtSF`) to represent the true size of the property.
* **`HouseAge`:** Calculated as the age of the house at the time of sale (`YrSold` - `YearBuilt`), which is more informative than the construction year.
* **`TotalBath`:** Aggregates all full and half bathrooms (above and below ground) into a single metric.

### Encoding

All remaining categorical data was converted into a numeric format:
* **Ordinal Encoding:** Applied to features with a clear rank (quality/condition) (e.g., mapping `Ex` $\rightarrow$ 5, `None` $\rightarrow$ 0).
* **One-Hot Encoding:** Applied to nominal categorical features (e.g., `Neighborhood`, `MSZoning`). This process created binary columns to eliminate false assumptions of order or magnitude. This resulted in a **high-dimensional feature space**.

***

## 3. Model Training & Comparison 🚀

With over 200 features, the prepared dataset was split and scaled using `StandardScaler`. Various regression algorithms were trained to benchmark performance.

### Model Benchmarking Results

Model performance was rigorously compared using the **Root Mean Squared Error (RMSE)** in dollar terms and the **R-squared ($R^2$)** score.

| Model | RMSE (Mean Error) | R-squared Score ($R^2$) |
| :---: | :---: | :---: |
| Linear Regression (Baseline) | \$21,943.75 | 0.9211 |
| **Lasso Regression** | **\$20,983.34** | **0.9278** |
| Random Forest Regressor | \$24,500.84 | 0.9016 |
| XGBoost Regressor | \$22,535.00 | 0.9168 |

### Conclusion on the Winning Model: Lasso Regression

The **Lasso Regression** model achieved the **lowest RMSE (\$20,983.34)** and the **highest $R^2$ score (0.9278)**, making it the top-performing candidate.

The Lasso model excelled due to its use of the **$L1$ regularization penalty**. This penalty automatically performs **feature selection** by forcing the coefficients of irrelevant or noisy features (many of the dummy variables) to become *exactly zero*. This pruning process successfully reduced noise and complexity, allowing Lasso to generalize better than the more complex Ensemble models.

***

## 4. Hyperparameter Tuning & Feature Importance 📈

The final stage involved optimizing the Lasso model and assessing its interpretability.

### Hyperparameter Tuning

**Goal:** Find the optimal regularization strength, **`alpha` ($\alpha$)**, for the Lasso model.

**Method:** A **Grid Search** was performed with **5-Fold Cross-Validation** (`GridSearchCV`) across a logarithmic range of $\alpha$ values.

**Result (Tuned Model):**
* The optimal $\alpha$ used for the final model was **$0.002807$**.
* The final model achieved an RMSE of **\$21,316.18** and an $R^2$ of **0.9255** on the test set.

### Feature Importance Analysis

For Lasso, **feature importance** is determined by the **magnitude** (absolute value) of the scaled coefficient. The analysis confirms the success of the feature engineering and the inherent drivers of house price.

The top 5 most influential predictors are:

| Rank | Feature |
| :---: | :---: |
| 1 | **`OverallQual`** |
| 2 | **`TotalSqFt`** |
| 3 | **`GrLivArea`** |
| 4 | **`Neighborhood_NridgHt`** |
| 5 | **`GarageCars`** |

This clear hierarchy of features confirms the model is both highly accurate and easily interpretable, validating the entire preprocessing and modeling pipeline.