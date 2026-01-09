import streamlit as st
import os
import tempfile
from dotenv import load_dotenv

# Import identici al TUO codice funzionante (LCEL Puro)
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. Configurazione Iniziale
load_dotenv()
st.set_page_config(page_title="RAG Chatbot", layout="wide")
st.title("🧠 Chatbot Documentale (RAG)")

# 2. Gestione Sidebar e Caricamento File
with st.sidebar:
    st.header("📂 Carica Documento")
    uploaded_file = st.file_uploader("Carica il tuo PDF qui", type="pdf")
    
    if st.button("Pulisci Chat"):
        st.session_state.messages = []
        if "rag_chain" in st.session_state:
            del st.session_state.rag_chain

# 3. Funzione per elaborare il PDF e creare la Chain (Stile Vecchio Codice)
def create_chain_from_pdf(uploaded_file):
    with st.spinner("Sto leggendo e indicizzando il documento..."):
        # A. Salva file temporaneo
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.getbuffer())
            temp_file_path = temp_file.name

        # B. Caricamento e Chunking
        loader = PyPDFLoader(temp_file_path)
        docs = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(docs)

        # C. Vector Store (In memoria)
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
        retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
        
        # D. Costruzione Chain (IDENTICA al tuo codice funzionante)
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        
        template = """
        Rispondi alla domanda basandoti SOLO sul seguente contesto.
        Se non sai la risposta, dì "Non lo so".
        
        Contesto:
        {context}
        
        Domanda:
        {question}
        """
        prompt = ChatPromptTemplate.from_template(template)

        # LCEL Puro: Parallelismo per recuperare contesto E generare risposta
        chain = RunnableParallel(
            {"context": retriever, "question": RunnablePassthrough()}
        ).assign(answer=(
            prompt 
            | llm 
            | StrOutputParser()
        ))
        
        # Pulizia file
        os.remove(temp_file_path)
        
        return chain

# 4. Logica Principale
if uploaded_file:
    # Creiamo la chain solo se non esiste già o se è cambiato il file
    if "rag_chain" not in st.session_state:
        st.session_state.rag_chain = create_chain_from_pdf(uploaded_file)
        st.success("Documento pronto! Puoi fare domande.")
        st.session_state.messages = []

    # Inizializza cronologia
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostra messaggi precedenti
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input Utente
    if user_input := st.chat_input("Fai una domanda sul documento..."):
        # Mostra domanda
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Genera Risposta
        with st.chat_message("assistant"):
            with st.spinner("Sto cercando..."):
                # Invoca la Chain
                rag_chain = st.session_state.rag_chain
                result = rag_chain.invoke(user_input)
                
                response_text = result['answer']
                sources = result['context']
                
                # Mostra Risposta
                st.markdown(response_text)
                
                # Mostra Fonti (Stile del tuo vecchio codice)
                with st.expander("📚 Fonti utilizzate"):
                    for i, doc in enumerate(sources):
                        page_num = doc.metadata.get('page', 'N/D')
                        # Pulizia del testo per renderlo leggibile
                        clean_content = doc.page_content.replace("\n", " ").replace("  ", " ")
                        
                        st.markdown(f"**🔹 Fonte {i+1} (Pagina {page_num}):**")
                        st.caption(f"\"{clean_content[:1000]}...\"")
                        st.divider()

        # Salva nella cronologia
        st.session_state.messages.append({"role": "assistant", "content": response_text})

else:
    st.info("👈 Carica un PDF dalla barra laterale per iniziare.")