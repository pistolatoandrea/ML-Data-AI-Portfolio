import os
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
import csv

load_dotenv()

# --- Tool 1: Web Search (integrated in LangChain)---
search_tool = TavilySearchResults(
    max_results=3,
    description="Search the web for current information on a topic. Input should be a specific search query."
)

# --- Tool 2: Markdown File Writer ---
@tool
def save_report(content: str, filename: str = "outputs/report.md") -> str:
    """Save the final research report to a markdown file."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write(content)
    return f"Report saved to {filename}"

# --- Tool 3: CSV Writer ---

@tool
def save_sources_csv(search_results: list[str], filename: str = "outputs/sources.csv") -> str:
    """Save all research sources to a CSV file with URL and content columns."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    filepath = filename
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source_url", "content_snippet"])
        for result in search_results:
            lines = result.split("\n", 1)
            url = lines[0].replace("Source: ", "").strip()
            content = lines[1].strip() if len(lines) > 1 else ""
            writer.writerow([url, content[:300]])
    return f"Sources saved to {filepath} ({len(search_results)} entries)"