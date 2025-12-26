# Resume RAG Chatbot

A Retrieval-Augmented Generation (RAG) based chatbot that answers questions strictly from resume and certificate PDFs using semantic search and a local LLM, ensuring zero hallucination and full source traceability.

---

## Problem Statement

Traditional chatbots either rely on keyword-based search or large language models that may hallucinate answers.  
In scenarios like resume screening or document verification, hallucinated or assumed answers are unacceptable.

Recruiters and organizations need systems that provide **accurate, document-grounded answers** strictly based on verified data such as resumes and certificates.

This project solves that problem using **Retrieval-Augmented Generation (RAG)**.

---

## Solution Overview

The system ingests resume and certificate PDF documents, extracts text, splits it into smaller overlapping chunks, and converts those chunks into embeddings.

When a user asks a question, the system retrieves the most relevant chunks using semantic similarity from a vector database and generates a concise answer using a local LLM, strictly limited to the retrieved context.

If the information is not present in the documents, the system explicitly responds that the information is not mentioned, preventing hallucination.

---

## Architecture

PDF Documents  
→ Text Extraction (PyPDFLoader)  
→ Chunking (Recursive Character Text Splitter)  
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

- Retrieval-Augmented Generation (RAG) architecture
- Answers strictly grounded in document context
- Explicit anti-hallucination handling
- Source attribution for every response
- Fully local setup (no API keys required)
- Analytics logging for monitoring usage
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

1. Create and activate virtual environment
2. Install dependencies:
3. Start backend server:
uvicorn backend.main:app --reload

4. Open Swagger UI:
http://127.0.0.1:8000/docs
### Frontend

1. Run Streamlit app:



2. Open browser and start asking questions.

---

## Example Usage

**Question:**  
What certifications has Nikhil completed?

**Answer:**  
This information is not mentioned in the resume.

**Sources:**  
- resume_ats.pdf (page 1)

---

## Why RAG Instead of a Normal Chatbot

- Prevents hallucinated responses  
- Ensures trust and accuracy  
- Works on private, internal documents  
- Enables semantic search instead of keyword matching  
- Aligns with real-world enterprise GenAI systems  

---

## Analytics & Observability

The system logs:
- Total number of questions asked
- Question text
- Source documents used
- Timestamp of each query

This enables basic monitoring and future insights into usage patterns.

---

## Future Improvements

- Persistent embedding storage
- Multi-document intelligence
- Conversation memory
- Cloud deployment
- Authentication and access control
- Advanced analytics dashboard

---

## Conclusion

This project demonstrates an end-to-end, production-style GenAI system using Retrieval-Augmented Generation.  
It highlights practical skills in document processing, semantic search, local LLM integration, API development, and UI integration, making it suitable for real-world enterprise use cases.