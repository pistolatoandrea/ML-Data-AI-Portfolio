# 🧠 C1: Context-Aware RAG Chatbot

An intelligent virtual assistant based on **RAG (Retrieval-Augmented Generation)** architecture, designed to answer questions based on private corporate documents while minimizing hallucinations. The system does not just generate text; it "reads" a PDF manual, retrieves relevant information, and cites the exact sources.

### 🎯 Project Objective
To build a complete AI pipeline that demonstrates how to overcome the limitations of standard LLMs (lack of private knowledge, hallucinations) by integrating an external vector memory.

**Key Features:**
* **Ingestion Pipeline:** Loading, chunking, and indexing of PDFs.
* **Vector Database:** Using ChromaDB for local semantic search.
* **Anti-Hallucination:** Prompt engineering to strictly bind answers to the provided context.
* **Source Citation:** The UI displays exactly which page of the document was used to generate the answer.
* **Web Interface:** Modern UI built with Streamlit.

---

### 🛠️ Tech Stack
* **Orchestration:** LangChain (LCEL approach)
* **LLM & Embeddings:** OpenAI (GPT-3.5-turbo, text-embedding-3-small)
* **Vector Database:** ChromaDB (Local, persistent)
* **Frontend:** Streamlit
* **Data Processing:** PyPDF

---

### 📂 Project Structure

```bash
C1_Context_Aware_Chatbot/
├── data/                  # Folder containing source PDF documents
│   └── FT_COMPANY_OPERATING_MANUAL.pdf
├── db_chroma/             # Vector Database (automatically generated)
├── .env                   # Configuration file
├── ingest.py              # ETL Script: Load PDF -> Create Embeddings -> Save to DB
├── rag_bot.py             # CLI Script: Terminal chatbot for quick testing
├── app.py                 # Web App: Full GUI with Streamlit
├── requirements.txt       # Project dependencies
└── README.md              # Documentation
```

---

### 🚀 Installation Guide

**1. Clone the repository and prepare the environment**

```bash
# Enter the folder

cd C1_Context_Aware_RAG_Chatbot

# Create a clean virtual environment

python -m venv venv 

source venv/bin/activate # On MacOs

venv\Scripts\activate # On Windows

# Install dependencies

pip install -r requirements.txt
```

**2. Configure API Keys**

Create a file named *.env* in the root of the project and insert your *OpenAI key*:

Code snippet

    OPENAI_API_KEY=sk-proj-....................

(Note: Ensure you have available credit on your OpenAI API account).

---

### 💻 Usage

The project is divided into two phases: Ingestion (one-time) and Usage (chat).

**Phase 1: Data Ingestion (ETL)** 

Before chatting, we must transform the PDF into mathematical vectors.

```bash
python ingest.py
Expected Output: ✅ Done! Database saved in folder 'db_chroma'.
```

**Phase 2: Launch Web App**

Launch the graphical interface to interact with the chatbot.

```bash

python -m streamlit run app.py
The browser will automatically open at http://localhost:8501.

```

### 🧠 Key Concepts Implemented

1. Chunking Strategy Documents are not loaded as a whole. We use RecursiveCharacterTextSplitter with:

    **Chunk Size**: 1000 characters.

    **Overlap**: 200 characters (to maintain context between cuts and avoid losing information mid-sentence).

2. Semantic Search (vs Keyword Search) Unlike SQL (WHERE text LIKE '%holiday%'), we use Embeddings. If the user asks "Can I work from home?", the system finds the paragraph "Smart Working Policy" thanks to vector proximity, even if the exact words differ.

3. Retrieval Parameters (K=3) The system retrieves the 3 most relevant chunks for each question. This balances answer completeness with token costs and reduces the risk of the "Lost in the Middle phenomenon".

### 🔮 Future Improvements

**Dockerization**: 

Create a container for deployment on AWS/Azure.

**Multi-User Memory**: 

Add persistent chat history per user session.

**Scalability**:

Migrate from ChromaDB (local) to Pinecone (Cloud) to handle millions of vectors.

**Agents**:

Allow the bot to perform actions (e.g., sending a bug report email) instead of just explaining how to do it.    