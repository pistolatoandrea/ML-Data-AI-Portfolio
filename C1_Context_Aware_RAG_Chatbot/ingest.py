import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

# 1. Carica variabili d'ambiente (API Key)
load_dotenv()

# Configurazione
PERCORSO_PDF = "data/FT_COMPANY_OPERATING_MANUAL.pdf"
PERSIST_DIRECTORY = "db_chroma"

def ingest_documents():
    # --- 1: LOADING ---
    print(f"📄 Loading file: {PERCORSO_PDF}...")
    if not os.path.exists(PERCORSO_PDF):
        raise FileNotFoundError(f"File {PERCORSO_PDF} does not exist!")
        
    loader = PyPDFLoader(PERCORSO_PDF)
    docs = loader.load()
    print(f"{len(docs)} page founded.")

    # --- 2: SPLITTING ---
    print("✂️  Splitting in chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,      # target
        chunk_overlap=200,    # overlapping
        separators=["\n\n", "\n", " ", ""] # separators priority
    )
    chunks = text_splitter.split_documents(docs)
    print(f"   Creati {len(chunks)} chunks di testo.")

    # --- 3: EMBEDDING AND SAVING ---
    print("💾 Vector Database Creation...")
    
    # Intialize OpenAI Embedding Model (translate text to numbers)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # DB Creation and Files Saving
    db = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings, 
        persist_directory=PERSIST_DIRECTORY
    )
    
    print(f"✅ Database saved in '{PERSIST_DIRECTORY}'")

if __name__ == "__main__":
    ingest_documents()