# 📰 News Classification API: MLOps & Containerization

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Container-2496ED?logo=docker&logoColor=white)
![Render](https://img.shields.io/badge/Deployment-Render-46E3B7?logo=render&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/ML-Pipeline-F7931E?logo=scikit-learn&logoColor=white)

## 📌 Project Overview
This project represents **Phase B (MLOps)** of my Machine Learning portfolio.  
The goal was to evolve a static NLP model (from **Project A4**) into a production-ready, containerized Microservice accessible via REST API.

The project follows a rigorous engineering workflow: from local environment setup to refactoring, Docker troubleshooting, and finally Cloud Deployment.

---

## 📂 1. Project Structure
The repository is organized to separate the experimentation logic (`notebooks`) from the production logic (`app`).

## 🛠️ 2. Environment Setup
To ensure reproducibility locally, I created an isolated Python environment:

```bash
# Creation
python3 -m venv venv

# Activation (Mac/Linux)
source venv/bin/activate

# Dependencies
pip install -r requirements.txt
```

## ⚡ 3. The "Hello World" API
Before integrating the AI, I established the baseline infrastructure using **FastAPI** and **Uvicorn** to ensure the server could accept requests.

* **Server:** Uvicorn (ASGI)
* **Port:** 8000
* **Response:** Simple JSON `{"status": "Up and Running"}`

## 🔄 4. The Architecture Shift: From Scripts to Pipeline

**The Problem:** In the original Project A4, vectorization (TF-IDF) and classification were performed in separate steps. This created complexity for the API, which received raw text but needed to apply the exact same vocabulary transformation as training.

**The Decision:** I unified preprocessing and inference into a single Scikit-Learn Pipeline.

* **Old Flow:** `Input` -> `Vectorizer` -> `Vector` -> `Model` -> `Prediction`
* **New Flow:** `Input` -> `Pipeline(Vectorization + Model)` -> `Prediction`

## 🧠 5. Refactoring & Manual Continuous Deployment (CD)
I created a specialized notebook (`notebooks/refactor_pipeline.ipynb`) to generate the model artifact.

To handle updates (e.g., dataset changes) without breaking production, I implemented a **Dual-Save Strategy**:
1.  **Historical Archive:** Saves a timestamped copy in `app/model/versions/` (e.g., `model_20231027.pkl`).
2.  **Production Overwrite:** Automatically replaces `app/model/news_classifier.pkl`.

> **Result:** Rerunning the notebook instantly deploys the new logic to the API upon restart.

## 🧪 6. Local Integration Testing
With the new `.pkl` pipeline, I updated `app/main.py` to handle predictions.

* **Input:** Raw string (e.g., *"The match ended 2-0"*).
* **Process:** Loaded via `joblib`, the pipeline handles tokenization internally.
* **Output:** JSON Category (e.g., "Sport").

Tested successfully via Swagger UI at `http://localhost:8000/docs`.

## 🐳 7. Dockerization Workflow
To make the application portable, I containerized it using Docker.

### 7.1 Configuration
* **`.dockerignore`**: Created to exclude heavy/useless files (`venv`, `.git`, `notebooks`) from the image.
* **`Dockerfile`**: Defined the recipe based on `python:3.10-slim`.

### 7.2 Build and Run
```bash
docker build -t news-api .
docker run -d -p 8000:80 --name news-container news-api
```

### 7.3 🐛 Troubleshooting: The Crash
* **The Issue:** The container started but crashed immediately (`Exited (1)`).
* **The Diagnosis:** `docker logs` revealed a `ModuleNotFoundError`. The CMD instruction in the Dockerfile pointed to a wrong filename/path for the app entry point.
* **The Fix:**
    1.  Corrected the CMD path in Dockerfile.
    2.  Removed the old container (`docker rm`).
    3.  Rebuilt the image (`docker build`).
    4.  Relaunched. **Success.**

## ☁️ 8. Cloud Deployment
The service was deployed to **Render** directly from the GitHub repository.

* **Runtime:** Docker
* **Environment:** Auto-detected Dockerfile
* **Port:** Mapped public traffic to internal container port 80
* **Live URL SWAGGER UI:** [https://news-api-portfolio.onrender.com/docs](https://news-api-portfolio.onrender.com/docs)

## 📡 9. Client Testing
To simulate a real-world scenario (e.g., a frontend app calling the model), I wrote a Python script (`prediction_call.py`) using the `requests` library.

**Usage:**
```bash
python prediction_call.py
```

**Output:**
```plaintext
📡 Calling API...
✅ Success!
📝 Input: The government announced a new tax reform...
🏷️ Predicted Category: politics
```