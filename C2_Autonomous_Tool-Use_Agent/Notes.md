# C2 Projecg

## 1. Directory Progetto

- API KEY in .env
- requirements.txt
- VENV

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## 2. Graph

- **States**: what each node receives before activate
- **Tools**: Tavily search_tool (used by node 2) and custom @tool save_report (used by node 4)
- **Nodes**: define graph's nodes planner -> searcher -> evaluator -> writer
    - **Flow**: The agent takes a research task as input and breaks it down into specific search queries (Planner). It then searches the web for each query using Tavily (Searcher) and evaluates whether the collected information is comprehensive enough to write a report (Evaluator). If not, it runs another search iteration. Once satisfied — or after a maximum of 2 iterations — it synthesizes all findings into a structured markdown report and a csv file and saves them to disk (Writer).
- **Graph**: orchestration, build graph, nodes, fixed and conditional edges

## 3. Versioning

- New name and timestamp
- Folder Versioning


