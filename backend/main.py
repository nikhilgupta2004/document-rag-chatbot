from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
import json
from datetime import datetime

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.llms import Ollama
from sentence_transformers import SentenceTransformer
import chromadb


# ======================================================
# APP INIT
# ======================================================
app = FastAPI(title="Resume RAG Chatbot")


# ======================================================
# ANALYTICS (SAFE & STABLE)
# ======================================================
ANALYTICS_FILE = Path("analytics/logs.json")
ANALYTICS_FILE.parent.mkdir(exist_ok=True)

if not ANALYTICS_FILE.exists():
    ANALYTICS_FILE.write_text(
        json.dumps({"total_questions": 0, "logs": []}, indent=2)
    )


def log_question(question, sources):
    data = json.loads(ANALYTICS_FILE.read_text())

    data["total_questions"] += 1
    data["logs"].append({
        "question": question,
        "sources": sources,
        "time": datetime.now().isoformat()
    })

    ANALYTICS_FILE.write_text(json.dumps(data, indent=2))


# ======================================================
# LOAD DOCUMENTS
# ======================================================
DATA_DIR = Path("data")

documents = []
sources = []

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

for pdf in DATA_DIR.glob("*.pdf"):
    loader = PyPDFLoader(str(pdf))
    pages = loader.load()
    chunks = splitter.split_documents(pages)

    for chunk in chunks:
        documents.append(chunk.page_content)
        page_no = chunk.metadata.get("page", 0) + 1
        sources.append(f"{pdf.name} (page {page_no})")

# 🔒 SAFETY CHECK
if not documents:
    raise RuntimeError("No valid PDF documents found in data folder.")


# ======================================================
# EMBEDDINGS + VECTOR DB (FIXED)
# ======================================================
embedder = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = embedder.encode(documents).tolist()

client = chromadb.Client()

# ✅ IMPORTANT FIX: prevent duplicate collections
collection = client.get_or_create_collection("resume_rag")

# ✅ Avoid duplicate insertion on restart
if collection.count() == 0:
    for i in range(len(documents)):
        collection.add(
            documents=[documents[i]],
            embeddings=[embeddings[i]],
            metadatas=[{"source": sources[i]}],
            ids=[str(i)]
        )


# ======================================================
# LOCAL LLM (NO API KEY)
# ======================================================
llm = Ollama(model="phi")


# ======================================================
# REQUEST SCHEMA
# ======================================================
class Question(BaseModel):
    question: str


# ======================================================
# ASK ENDPOINT (FINAL, SAFE, RAG-CORRECT)
# ======================================================
@app.post("/ask")
def ask(payload: Question):

    query_embedding = embedder.encode(
        [payload.question]
    ).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3,
        include=["documents", "metadatas"]
    )

    context = ""
    used_sources = []

    for doc, meta in zip(
        results["documents"][0],
        results["metadatas"][0]
    ):
        context += doc[:700] + "\n"
        used_sources.append(meta["source"])

    prompt = f"""
You are a resume-based question answering system.

STRICT RULES:
- Answer in ONLY ONE short sentence.
- Do NOT explain or assume anything.
- Use ONLY the information from Context.
- If information is not explicitly present, reply EXACTLY:
  This information is not mentioned in the resume.

Context:
{context}

Question:
{payload.question}

Final Answer:
"""

    answer = llm.invoke(prompt).strip()

    # 🔒 HARD ANTI-HALLUCINATION OVERRIDE
    if any(x in answer.lower() for x in [
        "sorry", "not able", "unable", "cannot", "i don't know"
    ]):
        answer = "This information is not mentioned in the resume."

    final_sources = list(set(used_sources))
    log_question(payload.question, final_sources)

    return {
        "answer": answer,
        "sources": final_sources
    }
