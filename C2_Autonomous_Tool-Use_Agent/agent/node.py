import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from .state import AgentState
from .tools import search_tool, save_report
from .tools import search_tool, save_report, save_sources_csv
from datetime import datetime
import json

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0)

# -- Node 1: Planner --

def planner(state: AgentState) -> dict:
    messages = [
        SystemMessage(content="""You are a research planning assistant.
        Given a research task, break it down into 3-4 specific search queries
        that together will provide comprehensive coverage of the topic.
        Return ONLY a Python list of strings, nothing else.
        Example: ["query 1", "query 2", "query 3"]"""),
        HumanMessage(content=f"Research task: {state['task']}")
    ]
    
    response = llm.invoke(messages)
    
    subtasks = eval(response.content)
    
    return {"subtasks": subtasks, "iterations": 0}

# -- Node 2: Searcher --

def searcher(state: AgentState) -> dict:
    results = []
    
    for query in state["subtasks"]:
        search_results = search_tool.invoke(query)
        # ogni risultato è un dict con "url" e "content"
        for r in search_results:
            results.append(f"Source: {r['url']}\n{r['content']}")
    
    return {"search_results": results}

# -- Node 3: Evaluator --

def evaluator(state: AgentState) -> dict:
    # se abbiamo già fatto 2 iterazioni, forziamo l'uscita
    if state["iterations"] >= 2:
        return {"iterations": state["iterations"]}
    
    all_results = "\n\n".join(state["search_results"])
    
    messages = [
        SystemMessage(content="""You are a research quality evaluator.
        Given a research task and collected information, determine if the 
        information is sufficient to write a comprehensive report.
        Reply with ONLY 'sufficient' or 'insufficient'."""),
        HumanMessage(content=f"""Task: {state['task']}
        
Collected information:
{all_results[:3000]}""")  # limitiamo per non sprecare token
    ]
    
    response = llm.invoke(messages)
    verdict = response.content.strip().lower()
    
    return {
        "iterations": state["iterations"] + 1,
        "subtasks": [] if verdict == "sufficient" else state["subtasks"]
    }

# -- Node 4: Writer --

def writer(state: AgentState) -> dict:
    all_results = "\n\n".join(state["search_results"])
    
    # --- chiedi all'LLM un nome parlante per la run ---
    
    name_messages = [
        SystemMessage(content="""Generate a short, filesystem-safe folder name (max 4 words, lowercase, underscores) 
        that describes this research task. Return ONLY the name, nothing else.
        Example: 'edtech_europe_trends_2025'"""),
        HumanMessage(content=f"Research task: {state['task']}")
    ]
    name_response = llm.invoke(name_messages)
    run_name = name_response.content.strip().replace(" ", "_").replace("-", "_")
    
    # --- costruisci il path della run ---
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_folder = f"outputs/{timestamp}_{run_name}"
    os.makedirs(run_folder, exist_ok=True)
    
    # --- genera il report ---
    messages = [
        SystemMessage(content="""You are a professional research report writer.
        Write a comprehensive, well-structured markdown report based on the 
        research findings provided. Include:
        - Executive Summary
        - Key Findings (with sections)
        - Conclusions
        Use proper markdown formatting with headers, bullet points, and emphasis."""),
        HumanMessage(content=f"Research task: {state['task']}\n\nResearch findings:\n{all_results}")
    ]
    response = llm.invoke(messages)
    report_content = response.content
    
    # --- salva report e csv ---
    save_report.invoke({
        "content": report_content,
        "filename": f"{run_folder}/report.md"
    })
    save_sources_csv.invoke({
        "search_results": state["search_results"],
        "filename": f"{run_folder}/sources.csv"
    })
    
    # --- salva metadata ---
    metadata = {
        "task": state["task"],
        "timestamp": timestamp,
        "run_name": run_name,
        "iterations": state["iterations"],
        "sources_count": len(state["search_results"]),
        "output_folder": run_folder
    }
    with open(f"{run_folder}/run_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    return {"report": report_content, "run_folder": run_folder}