import os
import sys
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

PERSIST_DIRECTORY = "db_chroma"

def start_chat():
    print("🤖 Initializing RAG Chatbot (with Sources)...")

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    embedding_function = OpenAIEmbeddings(model="text-embedding-3-small")
    
    if not os.path.exists(PERSIST_DIRECTORY):
        print(f"❌ Error: DB not found.")
        sys.exit(1)

    db = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embedding_function)
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})

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

    # --- CAMBIAMENTO CHIAVE: LA CATENA ---
    # Invece di restituire solo la stringa, usiamo RunnableParallel
    # per mantenere vivo l'oggetto "context" (i documenti) fino alla fine.
    rag_chain_with_source = RunnableParallel(
        {"context": retriever, "question": RunnablePassthrough()}
    ).assign(answer=(
        prompt 
        | llm 
        | StrOutputParser()
    ))

    print("✅ Ready! Type 'exit' to stop.")
    print("-" * 50)

    while True:
        query = input("\nYou: ")
        if query.lower() in ["exit", "quit", "esci"]:
            break
        
        print("🤖 Thinking...", end="\r")
        
        # Ora 'result' è un dizionario che contiene sia la risposta che i documenti
        result = rag_chain_with_source.invoke(query)
        
        print(" " * 50, end="\r") # Pulisce la riga
        
        # 1. Stampa la risposta
        print(f"Bot: {result['answer']}")
        
        # 2. Stampa le fonti (Debug/Explainability)
        print("\n   [Sources used:]")
        for i, doc in enumerate(result['context']):
            # Otteniamo il nome del file e la pagina dai metadati
            source_name = doc.metadata.get('source', 'Unknown')
            page_num = doc.metadata.get('page', 'Unknown')
            # Stampiamo un'anteprima del contenuto (primi 50 caratteri)
            content_preview = doc.page_content[:50].replace("\n", " ")
            print(f"   {i+1}. {source_name} (Page {page_num}): \"{content_preview}...\"")

if __name__ == "__main__":
    start_chat()