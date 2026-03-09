from agent.graph import build_graph

graph = build_graph()

result = graph.invoke({
    "task": "provide a report on european sport entertainment trend of 2025",
    "subtasks": [],
    "search_results": [],
    "report": "",
    "iterations": 0
})

print(result["report"])