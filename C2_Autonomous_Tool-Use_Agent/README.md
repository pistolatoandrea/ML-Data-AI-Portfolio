# C2 — Autonomous Research & Report Agent

> An LLM-powered agent that autonomously plans, searches, evaluates, and writes structured research reports from a single natural language prompt.

---

## Overview

This project implements an **autonomous tool-use agent** using LangGraph and GPT-4o. Given a research task in plain English, the agent breaks it down into search queries, retrieves information from the web, evaluates whether the results are comprehensive enough, and iterates if needed — before synthesizing everything into a structured markdown report saved to disk.

The agent runs entirely autonomously once the task is provided. No manual step-by-step prompting required.

**Agent flow:**

> The agent takes a research task as input and breaks it down into specific search queries (Planner). It then searches the web for each query using Tavily (Searcher) and evaluates whether the collected information is comprehensive enough to write a report (Evaluator). If not, it runs another search iteration. Once satisfied — or after a maximum of 2 iterations — it synthesizes all findings into a structured markdown report and saves it to disk (Writer).

```
[START] → Planner → Searcher → Evaluator ──(sufficient)──→ Writer → [END]
                    ↑                                    
                    └─(insufficient)─┘
```

---

## Key Concepts Demonstrated

- **LangGraph** — explicit stateful graph orchestration with nodes, edges, and conditional routing
- **Tool use / function calling** — LLM autonomously decides when and how to invoke tools
- **Multi-step planning** — task decomposition into structured sub-queries before execution
- **Iterative reasoning loop** — agent self-evaluates output quality and decides whether to search again
- **Real API integration** — Tavily Search API for live web retrieval
- **Structured output** — every run produces a markdown report + CSV of sources + JSON metadata
- **Versioned run management** — each run is saved in a timestamped, LLM-named folder under `outputs/`
- **Observable UI** — Streamlit interface shows every agent decision step by step

---

## Tech Stack

| Component | Technology |
|---|---|
| LLM | GPT-4o (OpenAI API) |
| Agent Framework | LangGraph |
| Web Search | Tavily Search API |
| Output formats | Markdown report, CSV sources, JSON metadata |
| UI | Streamlit |
| Language | Python 3.11+ |

---

## Project Structure

```
C2_Autonomous_Tool-Use_Agent/
├── agent/
│   ├── __init__.py
│   ├── state.py        # AgentState TypedDict — shared state across nodes
│   ├── nodes.py        # Planner, Searcher, Evaluator, Writer nodes
│   ├── tools.py        # Tavily search tool, file writer, CSV exporter
│   └── graph.py        # LangGraph graph assembly and compilation
├── app.py              # Streamlit interface
├── main.py             # CLI entry point for testing
├── outputs/            # One versioned folder per run
│   └── 20260309_143022_example_query/
│       ├── report.md
│       ├── sources.csv
│       └── run_metadata.json
├── requirements.txt
├── .env.example
└── README.md
```

---

## How It Works — Node by Node

### 1. Planner
Receives the user's task and instructs GPT-4o to decompose it into 3–4 focused search queries. Returns a list of subtasks written into the shared State.

### 2. Searcher
Iterates over the subtasks and calls the Tavily Search API for each one. Results (URL + content snippet) are accumulated cumulatively in the State using LangGraph's `operator.add` annotation.

### 3. Evaluator
Reads all collected search results and asks GPT-4o whether the information is sufficient to write a comprehensive report. Returns `sufficient` or `insufficient`. A hard cap of 2 iterations prevents infinite loops. The routing decision (loop back to Searcher or proceed to Writer) is handled by a **conditional edge** in the graph.

### 4. Writer
Synthesizes all research findings into a structured markdown report with Executive Summary, Key Findings, and Conclusions. Asks GPT-4o to generate a short, descriptive folder name for the run, combines it with a timestamp, and saves three files into a dedicated versioned folder under `outputs/`:

- `report.md` — the full structured report in markdown
- `sources.csv` — all sources used, with URL and content snippet columns
- `run_metadata.json` — task, timestamp, run name, iteration count, source count

This means every run is fully reproducible and auditable, and no output is ever overwritten.

---

## Setup

### Prerequisites
- Python 3.11+
- OpenAI API key
- Tavily API key (free tier available at [tavily.com](https://tavily.com))

### Installation

```bash
# Clone the repo
git clone https://github.com/pistolatoandrea/ML-Data-AI-Portfolio.git
cd ML-Data-AI-Portfolio/C2_Autonomous_Tool-Use_Agent

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your API keys
```

### Environment Variables

```
OPENAI_API_KEY=your_openai_key_here
TAVILY_API_KEY=your_tavily_key_here
```

---

## Usage

### CLI (for testing)

```bash
python3 main.py
```

### Streamlit UI

```bash
streamlit run app.py
```

Enter your research task in the input field and watch the agent work through each step. The Activity panel shows every node execution and decision in sequence. Once complete, the UI displays three tabs: the rendered report, a searchable sources table, and run metadata — with download buttons for the report and CSV.

---

## Example

**Input task:**
```
Analyze the main trends in the European EdTech market in 2025
```

**Agent activity log:**
```
🧠 Planner    → Generated 3 search queries: EdTech Europe trends 2025, ...
🔍 Searcher   → Retrieved 9 new sources from the web
⚖️  Evaluator  → Verdict: insufficient — starting iteration 2
🔍 Searcher   → Retrieved 9 new sources from the web
⚖️  Evaluator  → Verdict: sufficient — proceeding to report writing
✍️  Writer     → Report generated and saved to outputs/20250309_143022_edtech_europe_trends
✅  Done       → Run complete
```

**Output files:**
```
outputs/20260309_143022_edtech_europe_trends/
├── report.md           # structured markdown report
├── sources.csv         # 18 sources with URL and content snippet
└── run_metadata.json   # task, timestamp, 2 iterations, 18 sources
```

---

## Possible Extensions

- Generate refined search queries on the second iteration instead of reusing the same ones
- Add a `Reader` tool to parse and extract content from specific URLs
- Support PDF export of the final report
- Add memory across sessions to build on previous research

---

## What I Learned

- How to model agent logic as an **explicit stateful graph** with LangGraph, as opposed to implicit loop-based agents
- The difference between fixed edges and **conditional edges** for dynamic routing
- How **tool decoration** works in LangChain and why docstrings are operational instructions for the LLM
- How to design **versioned output management** with timestamped folders and run metadata
- Best practices for **API key management** in Python projects (`python-dotenv`, `.env.example`, `pip freeze`)
- How to build an **observable agent UI** in Streamlit that exposes internal reasoning to non-technical users
- Why `operator.add` in LangGraph State enables **cumulative result accumulation** across loop iterations
