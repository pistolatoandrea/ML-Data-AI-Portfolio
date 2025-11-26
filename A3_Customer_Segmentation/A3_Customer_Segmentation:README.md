# 🛍️ Project A3: Customer Segmentation (Unsupervised Learning)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Library](https://img.shields.io/badge/Library-Scikit--Learn-orange)
![Visualization](https://img.shields.io/badge/Visualization-Plotly%20%7C%20Seaborn-purple)

## 📖 Project Overview

This project focuses on **Unsupervised Machine Learning** to identify distinct customer segments within a mall's dataset. Unlike supervised learning, we discover hidden patterns and structures in the data to understand **who** the customers are without predefined labels.

The analysis moves from basic exploratory analysis to advanced **K-Means Clustering**, validated by **Silhouette Scores**, and visualized using **PCA (Principal Component Analysis)** and **Interactive 3D Plots**.

---

## 🎯 Business Objective

The goal is to empower the marketing team to optimize resource allocation by targeting specific customer groups:
* **High-Value Customers (VIPs):** For loyalty programs.
* **Budget-Conscious Shoppers:** For discount campaigns.
* **Inactive/Low-Spenders:** For re-engagement strategies.

---

## 📸 Visualizations & Analysis

### 1. Exploratory Data Analysis (EDA)

Understanding the data distribution and relationships before modeling.

**A. Univariate Analysis (Distributions)**

![EDA Distributions](./Customer_Segmentation_Images/EDA_Univariate_Density.png)
*Distribution of Age, Annual Income, and Spending Score.*

**B. Bivariate Analysis (Income vs. Spending)**

![EDA Scatter](./Customer_Segmentation_Images/EDA_Scatterplot.png)
*The critical "Money Plot" showing potential natural clusters.*

**C. Multivariate Analysis (Pairplot)**

![EDA Pairplot](./Customer_Segmentation_Images/EDA_Pairplot.png)
*Pairwise relationships colored by Gender to inspect overlaps.*

---

### 2. Defining the Optimal K (Cluster Selection)

We used two mathematical methods to validate that **K=5** is the optimal number of segments.

| Method 1: The Elbow Method | Method 2: Silhouette Score |
| :---: | :---: |
| ![Elbow Method](./Customer_Segmentation_Images/2D_Elbow_Method.png) | ![Silhouette Score](./Customer_Segmentation_Images/2D_Silhouette_Score.png) |
| *The "Elbow" appears clearly at K=5.* | *Highest separation score achieved at K=5.* |

---

### 3. 2D Customer Segmentation (Final Model)

![Final 2D Clusters](./Customer_Segmentation_Images/2D_K-Means_Clustering_Scatterplot.png)
*Final visualization of the 5 customer segments based on Income and Spending Score.*

---

### 4. PCA Customer Segmentation (Dimensionality Reduction)

Since we included **Age** in the final model (3 variables), we used PCA to project the data into 2D space.
![PCA Clusters](./Customer_Segmentation_Images/PCA_Clusters.png)
*Data projected onto Principal Components. Note how the "Age" factor changes the cluster shapes compared to the simple 2D plot.*

---

### 5. Loadings Analysis (Interpretation)

To understand what the PCA axes actually mean, we analyzed the feature loadings.
![Feature Loadings](./Customer_Segmentation_Images/Feature_Loadings.png)
* **PC1 (X-Axis):** Represents "Generational Conservatism" (Older people spend less, Younger people spend more).
* **PC2 (Y-Axis):** Represents pure "Wealth" (Annual Income).

---

## 📊 Key Results: Customer Personas
Based on the analysis, we identified 5 distinct profiles:

| Cluster Label | Persona Name | Characteristics | Strategy |
| :---: | :--- | :--- | :--- |
| **0** | **Balanced Buyers** | Average Income, Average Spending. | Standard promotions & Nudging. |
| **1** | **Golden Geese** | High Income, High Spending. | **VIP Treatment**, Exclusive offers. |
| **2** | **Careless Spenders** | Low Income, High Spending (Young). | Impulse buy offers, Flash sales. |
| **3** | **Cautious Wealth** | High Income, Low Spending (Older). | Focus on Quality & Value proposition. |
| **4** | **Budget Watchers** | Low Income, Low Spending. | Clearance sales, low-cost recommendations. |

---

## ⚙️ How to Run
1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install pandas numpy matplotlib seaborn scikit-learn plotly nbformat
    ```
3.  Run the Jupyter Notebook `A3_Customer_Segmentation.ipynb`.