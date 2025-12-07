# 📰 News Classification API: From Experiment to Production

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![Docker](https://img.shields.io/badge/Docker-Container-blue)
![Sklearn](https://img.shields.io/badge/Sklearn-Pipeline-orange)

## 📌 Project Overview
This project represents **Phase B (MLOps & Deployment)** of my Machine Learning portfolio. 

The goal is to operationalize a trained NLP Classification Model (originally developed in **Project A4**) by converting it from a static Jupyter Notebook into a scalable, portable **REST API**. 

Unlike a standard Data Science project, this repository focuses on **Model Refactoring** and **Artifact Management**, ensuring the transition from "Experiment" to "Production-ready Microservice" is robust and reproducible.

### 🎯 Key Objectives
1.  **Model Refactoring:** Convert raw experimental code into a streamlined `scikit-learn Pipeline` to ensure consistent preprocessing between training and inference.
2.  **Version Control Strategy:** Implement a custom script for **Manual Continuous Deployment (CD)**, managing both historical model versions and the active production artifact.
3.  **Model Serving:** Expose the pipeline via HTTP endpoints using **FastAPI**.
4.  **Containerization:** (In Progress) Containerize the application using **Docker**.

---

## 📂 Project Structure

The project is organized to separate the **Experimentation/Refactoring** environment from the **Production Application**.

```text
project-b1-news-api/
│
├── app/                  # Application Source Code
│   ├── __init__.py
│   ├── main.py           # API Entry point (FastAPI)
│   └── model/            # Model Artifacts Store
│       ├── versions/            # 📂 Historical archives (e.g., model_20231205.pkl)
│       └── news_classifier.pkl  # 🚀 Active Production Model (Overwritten on update)
│
├── notebooks/            # Experimentation & Refactoring
│   ├── bbc-text.csv             # Raw Dataset
│   └── refactor_pipeline.ipynb  # Notebook for Pipeline creation & Versioning logic
│
├── Dockerfile            # Container instructions
├── requirements.txt      # Dependencies
└── README.md             # Documentation
```

 ## ⚙️ MLOps Architecture & Logic

 ### 1. The Inference Pipeline

In the original experiment (Project A4), vectorization (TF-IDF) and classification (Naive Bayes) were separate steps. In this production version, I refactored them into a single Pipeline object.

*Problem*: Serving raw models requires the API to manually replicate preprocessing steps (cleaning, vectorization), leading to code duplication and potential "Training-Serving Skew".

*Solution*: The scikit-learn Pipeline encapsulates preprocessing and inference. The API receives raw text strings, and the pipeline handles transformations automatically using the exact logic defined during training.

### 2. Manual CD & Versioning Strategy

To handle dataset updates or model retraining without breaking the API, the refactor_pipeline.ipynb notebook implements a Dual-Save Strategy:

*Historical Archive*: Every training run saves a timestamped artifact in app/model/versions/ (e.g., news_classifier_20231027_153000_acc98.pkl). This allows for rollback if needed.

*Production Deployment*: The script automatically overwrites app/model/news_classifier.pkl. The FastAPI server is configured to always load this specific file.

*Result*: Rerunning the notebook effectively deploys the new model to the "app" folder instantly.