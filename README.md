# Generic Document RAG System

A **Retrieval-Augmented Generation (RAG)** based chatbot that answers questions **strictly from provided PDF documents** using semantic search and a local LLM, ensuring **zero hallucination** and **full source traceability**.

The system is **document-agnostic** and can be used with resumes, certificates, policies, reports, manuals, or any other PDFs without changing the core code.

---

## Problem Statement

Traditional chatbots either rely on keyword-based search or large language models that may hallucinate answers.  
In document-sensitive scenarios such as resume screening, certificate verification, policy lookup, or compliance checks, hallucinated or assumed answers are unacceptable.

Organizations require systems that provide **accurate, document-grounded answers** strictly based on verified content.

This project solves that problem using **Retrieval-Augmented Generation (RAG)**.

---

## Solution Overview

The system ingests PDF documents, extracts text, splits it into smaller overlapping chunks, and converts those chunks into vector embeddings.

When a user asks a question, the system retrieves the most relevant chunks using **semantic similarity search** from a vector database and generates a concise answer using a **local LLM**, strictly limited to the retrieved context.

If the requested information is not present in the documents, the system explicitly responds that the information is not mentioned, preventing hallucination.

---

## Architecture

PDF Documents  
→ Text Extraction (PyPDFLoader)  
→ Chunking (RecursiveCharacterTextSplitter)  
→ Embeddings (SentenceTransformer)  
→ Vector Database (ChromaDB)  
→ Semantic Retrieval  
→ Local LLM (Ollama)  
→ Final Answer + Source Attribution  

---

## Tech Stack

- **Backend:** FastAPI  
- **Frontend:** Streamlit  
- **Document Loader:** LangChain PyPDFLoader  
- **Text Chunking:** RecursiveCharacterTextSplitter  
- **Embeddings:** SentenceTransformer (all-MiniLM-L6-v2)  
- **Vector Database:** ChromaDB  
- **LLM:** Ollama (phi)  
- **Analytics:** JSON-based logging (query count, timestamps, sources)

---

## Key Features

- Generic document-based RAG architecture  
- Answers strictly grounded in document context  
- Explicit anti-hallucination handling  
- Source attribution for every response  
- Fully local setup (no API keys required)  
- Analytics logging for observability  
- Clean separation of backend and frontend components  

---

## Folder Structure

rag_resume_chatbot/
├── backend/
│ ├── main.py
│ └── requirements.txt
├── frontend/
│ └── app.py
├── data/
│ ├── resume_ats.pdf
│ ├── certificate.pdf
│ └── id_card.pdf
├── analytics/
│ └── logs.json
├── venv/
└── README.md
## How to Run Locally

### Backend

1. Create and activate a virtual environment  
2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt

   Start the backend server:

uvicorn backend.main:app --reload


Open Swagger UI:

http://127.0.0.1:8000/docs

Frontend

Run the Streamlit application:

streamlit run frontend/app.py


Open the browser and start asking questions.

Example Usage

Question:
What certifications has Nikhil completed?

Answer:
This information is not mentioned in the documents.

Sources:

resume_ats.pdf (page 1)

Why RAG Instead of a Normal Chatbot

Prevents hallucinated responses

Ensures trust and explainability

Works on private and internal documents

Enables semantic search instead of keyword matching

Matches real-world enterprise GenAI architectures

Analytics & Observability

The system logs:

Total number of questions asked

Question text

Source documents used

Timestamp of each query

This enables basic monitoring and future insights into usage patterns.

Supported Use Cases

Resume and certificate verification

Company policy and handbook Q&A

Academic notes and research papers

Internal documentation assistant

Compliance and legal document exploration

Future Improvements

Persistent embedding storage

Multi-document intelligence

Conversation memory

Cloud deployment

Authentication and role-based access

Advanced analytics dashboard

Conclusion

This project demonstrates an end-to-end, production-style Generic Document RAG System.
It highlights practical skills in document processing, semantic search, vector databases, local LLM integration, API development, and UI design, making it suitable for real-world enterprise GenAI use cases.
