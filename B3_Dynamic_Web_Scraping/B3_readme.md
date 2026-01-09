# Dynamic Web Scraping Pipeline

## 📖 Description
This project is part of a **Data Engineering & AI** portfolio consisting of 10 practical projects.
The goal is to build an **automated data ingestion pipeline** capable of extracting information from dynamic websites (Single Page Applications) that rely on JavaScript for content rendering.

Unlike static scraping (`requests` + `BeautifulSoup`), this script leverages **Selenium** to simulate a real browser, interact with the DOM, handle pagination, and persist data following **Data Lake** architecture principles (Raw/Bronze and Clean/Silver layers).

## 🎯 Project Objective
To extract quotes, authors, and metadata from the sandbox website [Quotes to Scrape (JS)](https://quotes.toscrape.com/js/), overcoming client-side rendering limitations and structuring the data for future analysis.

## ⚙️ Architecture & Features

### 1. Robust Navigation (Smart Waits)
The script avoids hardcoded timers (`sleep`) in favor of **Explicit Waits** (`WebDriverWait`). It dynamically waits for specific DOM elements to be visible before taking action, making the scraper resilient to varying network speeds.

### 2. Pagination Logic
Implementation of a `While` loop that:
* Scans the current page.
* Locates the "Next" button.
* Executes pure JavaScript (`execute_script`) to perform the click (bypassing potential overlays).
* Automatically breaks the loop when the last page is reached.

### 3. User Simulation & Headless Execution
* **User-Agent Spoofing:** Masks the bot as a real user running Chrome on Windows.
* **Headless Mode:** Runs Chrome in the background without a GUI to optimize resources (Server/Docker ready).

### 4. Data Lake Simulation (Bronze & Silver Layers)
Data is saved simulating a real ETL pipeline with temporal versioning:
* **🟤 Bronze Layer (Raw):** Raw data in `.json` format (preserving original structure and types).
* **⚪ Silver Layer (Clean):** Cleaned data (special character removal, normalization) in `.csv` format.
* **Versioning:** Files include a timestamp in the filename (e.g., `quotes_raw_20231027_1530.json`) to maintain history and ensure immutability.

## 🚀 How to Run

**Environment Setup**

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Run the Script**

```bash
python final_scraper.py
Check Output: Verify the data/ folder to see the generated JSON and CSV files.
```

# 🧠 Key Concepts Learned

**Client-Side vs. Server-Side Rendering**: Understanding when to use Selenium vs. standard Requests.

**DOM Manipulation**: Navigating the Document ObjectModel tree instead of parsing static HTML.

**Anti-Ban Strategies**: Using User-Agents and random delays.

**Data Engineering Principles**: Raw data immutability and Bronze/Silver layering.