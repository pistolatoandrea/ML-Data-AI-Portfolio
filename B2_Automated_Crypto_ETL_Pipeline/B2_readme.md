# Automated Crypto ETL Pipeline

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Prefect](https://img.shields.io/badge/Prefect-Orchestration-orange)
![Docker](https://img.shields.io/badge/Docker-Containerization-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Data_Warehouse-336791)
![Metabase](https://img.shields.io/badge/Metabase-BI_Dashboard-509EE3)

An end-to-end Data Engineering pipeline that extracts real-time cryptocurrency financial data, transforms it for analysis, loads it into a Data Warehouse, and visualizes trends via a BI Dashboard.

---

## 🏗 Architecture

The pipeline follows a modern **ELT (Extract, Load, Transform)** approach:

1.  **Ingestion:** A Python worker extracts data from the CoinGecko API (handling rate limits).
2.  **Storage:** Data is loaded into **PostgreSQL** (Dockerized), separated into:
    * **Bronze Raw Layer:** Immutable historical records.
    * **Gold Layer:** Transformed data (EUR conversion) ready for analytics.
3.  **Orchestration:** **Prefect** manages scheduling, retries, and observability.
4.  **Visualization:** **Metabase** connects to the DB to provide real-time price tracking charts.

### Key Engineering Decisions
* **Containerization:** Full isolation using Docker & Docker Compose for Database and BI tool.
* **Robustness:** Implemented exponential backoff strategies to handle API HTTP 429 (Rate Limits).
* **Idempotency:** The pipeline prevents duplicate data insertion during re-runs.

# 🚀 How to Run

### Prerequisites
* Docker Desktop installed & running
* Python 3.10+

## 1. Setup Environment

### Clone the main repository

### Activate virtual environment

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## 2. Start Infrastructure


**Start Docker containers (DB + Metabase)**

```bash
docker-compose up -d
```

**Start Prefect Server (in a separate terminal)**

```bash
prefect server start
```

### Run the Pipeline

```bash
python src/etl.py
```

### Access Dashboards

**Prefect UI**:
http://127.0.0.1:4200 (Pipeline health)

**Metabase UI**:
http://localhost:3000 (Data Visualization)

# 📈 Future Improvements

**Cloud Deployment**: Move Docker containers to AWS ECS or a generic VM.

**dbt Integration**: Move transformation logic from Pandas to dbt for better SQL modeling and lineage.

**Alerting**: Configure Prefect/Metabase to send Slack/Email alerts on price spikes.

# ⚙️ Debugging

**⚠️ Known Issue (Debugging in Progress)**: 

After a long period of inactivity, restarting the local scheduler triggered an unintended mass backfill of missed runs. This concurrency spike flooded the CoinGecko API, resulting in HTTP 429 (Too Many Requests) errors. I am currently debugging the Prefect deployment configuration to properly handle stale schedules and prevent this "thundering herd" effect upon restart.