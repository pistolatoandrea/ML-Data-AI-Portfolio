import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

# Importiamo i componenti di LangGraph
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

load_dotenv()

# --- 1. SETUP TOOL E LLM ---
@tool
def get_word_length(word: str) -> int:
    """Restituisce la lunghezza di una parola."""
    return len(word)

tools = [get_word_length]
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
llm_with_tools = llm.bind_tools(tools)

# --- 2. DEFINIZIONE DELLO STATO ---
# Lo stato è la "memoria" del grafo. È una lista di messaggi che cresce man mano.
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    # add_messages significa: "se arriva un messaggio nuovo, aggiungilo alla lista, non sovrascrivere"
    messages: Annotated[list, add_messages]

# --- 3. DEFINIZIONE DEI NODI ---

def call_model(state: AgentState):
    """Nodo che invoca l'LLM"""
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    # Restituiamo un dizionario che aggiorna lo stato
    return {"messages": [response]}

# Creiamo il nodo che esegue i tool automaticamente
tool_node = ToolNode(tools)

# --- 4. LOGICA CONDIZIONALE ---
def should_continue(state: AgentState):
    """Decide se fermarsi o eseguire un tool"""
    last_message = state["messages"][-1]
    # Se l'ultimo messaggio ha dei tool_calls, dobbiamo andare al nodo dei tool
    if last_message.tool_calls:
        return "tools"
    # Altrimenti abbiamo finito
    return END

# --- 5. COSTRUZIONE DEL GRAFO ---
workflow = StateGraph(AgentState)

# Aggiungiamo i nodi
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

# Definiamo l'entry point (da dove si parte)
workflow.set_entry_point("agent")

# Definiamo gli archi (flusso)
# Da "agent", decidiamo dove andare usando la funzione should_continue
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools", # Se should_continue ritorna "tools", vai al nodo "tools"
        END: END          # Se ritorna END, finisci
    }
)

# Dal nodo "tools", si torna SEMPRE all'agente (per fargli leggere il risultato)
workflow.add_edge("tools", "agent")

# Compiliamo il grafo
app = workflow.compile()

# --- 6. ESECUZIONE ---
input_message = HumanMessage(content="Quante lettere ha la parola 'Supercalifragilistichespiralidoso'?")
final_state = app.invoke({"messages": [input_message]})

# Stampiamo l'ultimo messaggio (la risposta finale)
print("\n--- RISPOSTA FINALE ---")
print(final_state["messages"][-1].content)