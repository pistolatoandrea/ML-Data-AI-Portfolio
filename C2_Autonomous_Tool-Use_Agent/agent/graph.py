from langgraph.graph import StateGraph, END
from .state import AgentState
from .node import planner, searcher, evaluator, writer

def route_after_evaluator(state: AgentState) -> str:
    """Routing function: choose next node after Evaluator."""
    if state["iterations"] >= 2:
        return "writer"
    if not state["subtasks"]:  # subtasks vuote = sufficient
        return "writer"
    return "searcher"

def build_graph():
    graph = StateGraph(AgentState)
    
    # --- nodes ---
    graph.add_node("planner", planner)
    graph.add_node("searcher", searcher)
    graph.add_node("evaluator", evaluator)
    graph.add_node("writer", writer)
    
    # --- fixed edges ---
    graph.set_entry_point("planner")
    graph.add_edge("planner", "searcher")
    graph.add_edge("searcher", "evaluator")
    graph.add_edge("writer", END)
    
    # --- conditional edge ---
    graph.add_conditional_edges(
        "evaluator",          # nodo di partenza
        route_after_evaluator, # routing function
        {                      # mappa stringa → nodo
            "writer": "writer",
            "searcher": "searcher"
        }
    )
    
    return graph.compile()