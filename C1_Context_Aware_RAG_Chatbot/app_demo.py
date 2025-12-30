import streamlit as st
import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# 1. Configurazione Pagina (Titolo, Icona)
st.set_page_config(page_title="Future-Tech HR Assistant", page_icon="🤖")

# Carica variabili d'ambiente
load_dotenv()

PERSIST_DIRECTORY = "db_chroma"

# --- FUNZIONI DI CACHING (Fondamentale per Streamlit) ---
# Streamlit riesegue l'intero script ogni volta che clicchi un bottone.
# Se non usassimo @st.cache_resource, ricaricherebbe il Database e il Modello
# a ogni singola domanda, rendendo tutto lentissimo.
@st.cache_resource
def load_rag_chain():
    """Carica la catena RAG una volta sola e la tiene in memoria."""
    
    # 1. Setup Embeddings
    embedding_function = OpenAIEmbeddings(model="text-embedding-3-small")
    
    # 2. Controllo DB
    if not os.path.exists(PERSIST_DIRECTORY):
        return None # Segnale di errore

    # 3. Carica Vector DB
    db = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embedding_function)
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})

    # 4. Setup LLM
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    # 5. Prompt
    template = """
    You are a helpful HR assistant for "Future-Tech".
    Use the provided context to answer. If unsure, say "I don't know".
    
    Context:
    {context}
    
    User Question:
    {question}
    
    Answer:
    """
    prompt = ChatPromptTemplate.from_template(template)

    # 6. Chain con Fonti
    chain = RunnableParallel(
        {"context": retriever, "question": RunnablePassthrough()}
    ).assign(answer=(
        prompt 
        | llm 
        | StrOutputParser()
    ))
    
    return chain

# --- INTERFACCIA UTENTE ---

st.title("🤖 Future-Tech AI Assistant")
st.caption("Ask questions about the internal operating manual.")

# Carichiamo la catena (grazie alla cache, è istantaneo dopo la prima volta)
rag_chain = load_rag_chain()

if rag_chain is None:
    st.error(f"Errore: Database non trovato in '{PERSIST_DIRECTORY}'. Esegui prima 'ingest.py'!")
    st.stop()

# --- GESTIONE MEMORIA CHAT (Session State) ---
# Streamlit non ha "memoria" nativa. Dobbiamo salvare noi la chat in session_state.
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! How can I help you with the company policies?"}]

# 1. Ridisegna tutta la chat precedente
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 2. Gestione Input Utente
if user_input := st.chat_input("Ask something (e.g., 'refund policy')..."):
    # A. Mostra messaggio utente
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # B. Genera risposta AI
    with st.chat_message("assistant"):
        with st.spinner("Searching manual..."):
            # Chiamata al RAG
            result = rag_chain.invoke(user_input)
            response_text = result['answer']
            sources = result['context']

            # Scrivi la risposta
            st.write(response_text)
            
            # Mostra le fonti in un menu a tendina (Expander)
            with st.expander("📚 View Sources"):
                for i, doc in enumerate(sources):
                    source_name = doc.metadata.get('source', 'Unknown').split('/')[-1]
                    page = doc.metadata.get('page', 'Unknown')
                    
                    # --- CORREZIONE QUI ---
                    # 1. Rimpiazza i caratteri di "a capo" (\n) con spazi vuoti
                    # 2. Rimpiazza eventuali doppi spazi creati dalla sostituzione
                    clean_content = doc.page_content.replace("\n", " ").replace("  ", " ")
                    
                    # Stampiamo un header più carino
                    st.markdown(f"**🔹 Source {i+1}:** `{source_name}` (Pag. {page})")
                    
                    # Stampiamo il testo pulito in corsivo o dentro un blocco info
                    st.info(f"\"...{clean_content[:1000]}...\"") 
                    # Ho aumentato l'anteprima a 300 caratteri per leggere meglio il contesto

    # C. Salva risposta AI nella memoria
    st.session_state.messages.append({"role": "assistant", "content": response_text})