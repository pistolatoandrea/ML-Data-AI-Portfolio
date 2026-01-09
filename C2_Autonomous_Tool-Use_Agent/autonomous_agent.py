import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
import yfinance as yf
from langchain_community.tools import DuckDuckGoSearchRun
import datetime
from langchain_core.messages import SystemMessage

load_dotenv()

# --- 1. DEFINIZIONE TOOLS ---

# TOOL 1: Web Search (Già pronto)
search = DuckDuckGoSearchRun()
# Creiamo un tool wrapper per dargli un nome e descrizione chiari per l'LLM
@tool
def web_search(query: str) -> str:
    """Cerca informazioni generiche o news recenti su internet (DuckDuckGo)."""
    return search.run(query)

# TOOL 2: Stock Price (Custom)
@tool
def get_stock_price(ticker: str) -> str:
    """
    Ottiene il prezzo attuale delle azioni per un dato ticker (es. AAPL, TSLA, NVDA).
    Restituisce solo il prezzo corrente e la valuta.
    """
    try:
        stock = yf.Ticker(ticker)
        # Data Engineering: L'API restituisce un JSON enorme.
        # Non passiamo tutto all'LLM (costa token e confonde). Estraiamo solo ciò che serve.
        price = stock.info.get('currentPrice')
        currency = stock.info.get('currency')
        return f"Il prezzo attuale di {ticker} è {price} {currency}."
    except Exception as e:
        return f"Errore nel recupero del prezzo per {ticker}: {e}"

# Lista dei tool disponibili
tools = [web_search, get_stock_price]

# --- 2. CONFIGURAZIONE LLM ---
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
llm_with_tools = llm.bind_tools(tools)

# --- 3. GRAFO (Identico a prima!) ---
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

def call_model(state: AgentState):
    messages = state["messages"]

    # 1. Calcoliamo la data di oggi dinamicamente
    now = datetime.datetime.now()
    date_str = now.strftime("%A, %d %B %Y") # Es: "Wednesday, 07 January 2026"
    
    # 2. Creiamo il System Prompt (La "Personalità" e il "Contesto")
    system_prompt = f"""
    Sei un Assistente Finanziario Senior di nome "WallStreetBot".
    
    REGOLE FONDAMENTALI:
    1. La data di oggi è: {date_str}. Tieni conto di questa data quando cerchi news o prezzi.
    2. Rispondi sempre in italiano, anche se le fonti (news) sono in inglese.
    3. Sii conciso e professionale. Usa elenchi puntati per i dati numerici.
    4. Se non trovi un dato preciso, dillo chiaramente, non inventare numeri.
    """
    
    # 3. Inseriamo il System Message PRIMA di tutti gli altri messaggi
    # Nota: Non lo aggiungiamo a 'state', lo usiamo solo per questa chiamata
    # per non riempire la memoria di messaggi di sistema ripetuti.
    full_history = [SystemMessage(content=system_prompt)] + messages

    response = llm_with_tools.invoke(full_history)
    return {"messages": [response]}

def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

tool_node = ToolNode(tools)

workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)
workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
workflow.add_edge("tools", "agent")

app = workflow.compile()

print("🤖 WallStreetBot è pronto! (Scrivi 'esci' per terminare)")
print("-" * 50)

# Inizializziamo la memoria della conversazione vuota
chat_history = []

while True:
    # 1. Input dell'utente
    user_input = input("\nTu: ")
    
    # Condizione di uscita
    if user_input.lower() in ["esci", "exit", "quit", "basta"]:
        print("👋 Alla prossima!")
        break
    
    # 2. Aggiungiamo il messaggio dell'utente alla storia
    # Nota: LangGraph gestisce lo stato, ma qui lo gestiamo manualmente 
    # per passarlo tra una chiamata e l'altra del "while" loop.
    chat_history.append(HumanMessage(content=user_input))
    
    # 3. Invochiamo l'Agente con TUTTA la storia accumulata finora
    # L'agente vedrà: [Domanda 1, Risposta 1, Domanda 2...]
    final_state = app.invoke({"messages": chat_history})
    
    # 4. Estraiamo la risposta finale dell'AI
    ai_response = final_state["messages"][-1].content
    
    # 5. Aggiorniamo la nostra storia locale con tutto quello che è successo
    # (inclusi i messaggi dei tool e la risposta finale dell'AI)
    chat_history = final_state["messages"]
    
    print(f"🤖 WallStreetBot: {ai_response}")

# --- 4. ESECUZIONE MULTI-STEP ---
# Chiediamo qualcosa che richiede DUE informazioni diverse
question = "Qual è il prezzo attuale delle azioni Apple (AAPL) e quali sono le ultime news sull'azienda?"

print(f"Domanda Utente: {question}\n")
final_state = app.invoke({"messages": [HumanMessage(content=question)]})

# --- DEBUGGING: VEDIAMO I PASSI ---
# Stampiamo tutti i messaggi per vedere il "ragionamento"
print("\n--- STORIA DEL RAGIONAMENTO ---")
for msg in final_state["messages"]:
    print(f"\n[{msg.type.upper()}]: {msg.content}")
    if hasattr(msg, 'tool_calls') and msg.tool_calls:
        print(f"   >>> HA CHIAMATO TOOL: {msg.tool_calls}")
