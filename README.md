# 📚 RAG Production App

An end-to-end **Retrieval-Augmented Generation (RAG)** application built using **FastAPI**, **Streamlit**, **Qdrant Vector Database**, and **Inngest workflows**.

This project allows users to upload PDF documents, generate embeddings, store them inside a vector database, and interact with the documents through an AI-powered chat interface.

---

# Features

-  Multi-PDF Upload Support
-  ChatGPT-style AI Chat Interface
-  Semantic Search using Vector Embeddings
-  FastAPI Backend
-  Streamlit Frontend
-  Qdrant Vector Database Integration
-  Event-Driven Workflows using Inngest
-  Context-Aware AI Responses
-  Source-Based Retrieval
-  Real-Time Streaming Response Effect
-  Modular Production-Style Backend Architecture

---

# Architecture

```text
Streamlit Frontend
        │
        ▼
FastAPI Backend
        │
        ▼
Inngest Workflows
        │
 ┌───────────────┐
 │ PDF Ingestion │
 └───────────────┘
        │
        ▼
Embedding Generation
        │
        ▼
Qdrant Vector DB
        │
        ▼
Semantic Retrieval
        │
        ▼
Gemini LLM Response
```

---

# Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core Development |
| FastAPI | Backend API |
| Streamlit | Frontend UI |
| Qdrant | Vector Database |
| Inngest | Workflow Orchestration |
| Gemini API | LLM Responses |
| OpenAI SDK | Gemini Integration |
| Pydantic | Data Validation |
| asyncio | Async Processing |

---

# Project Structure

```bash
RAGProductionApp/
│
├── app/
│   ├── core/
│   │   └── inngest_client.py
│   │
│   ├── db/
│   │   └── vector_db.py
│   │
│   ├── models/
│   │   └── custom_types.py
│   │
│   ├── services/
│   │   ├── data_loader.py
│   │   ├── embedding_service.py
│   │   ├── ingestion_service.py
│   │   ├── retrieval_service.py
│   │   └── llm_service.py
│   │
│   ├── workflows/
│   │   ├── ingest_workflow.py
│   │   └── query_workflow.py
│   │
│   └── main.py
│
├── frontend/
│   └── streamlit_app.py
│
├── README.md
├── requirements.txt
├── pyproject.toml
└── uv.lock
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/AdityaGupta62005/RAG-Production-App.git
cd RAGProductionApp
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

or using uv:

```bash
uv sync
```

---

# Environment Variables

Create a `.env` file in the root directory.

```env
OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
INNGEST_API_BASE=http://127.0.0.1:8288/v1
QDRANT_URL=http://localhost:6333
```

---

# Running the Application

## Start Qdrant

```bash
docker run -d --name qdrantRagDb -p 6333:6333 -v "$(pwd)/qdrant_storage:/qdrant/storage" qdrant/qdrant
```

---

## Start Inngest Dev Server

```bash
npx inngest-cli@latest dev -u http://127.0.0.1:8000/api/inngest --no-discovery
```

---

## Start FastAPI Backend

```bash
uv run uvicorn app.main:app --reload
```

---

## Start Streamlit Frontend

```bash
uv run streamlit run frontend/streamlit_app.py
```

---

# How It Works

## PDF Ingestion Workflow

1. User uploads PDF
2. PDF text is extracted
3. Text is chunked
4. Embeddings are generated
5. Chunks are stored in Qdrant

---

## Query Workflow

1. User asks a question
2. Query embedding is generated
3. Similar chunks are retrieved
4. Retrieved context is sent to Gemini
5. AI-generated answer is returned

---

# Key Concepts Used

- Retrieval-Augmented Generation (RAG)
- Semantic Search
- Vector Embeddings
- Chunking Strategies
- Event-Driven Architecture
- Durable AI Workflows
- Async Backend Processing

---

# Screenshots

## Chat Interface

<img width="1600" height="900" alt="logs" src="https://github.com/user-attachments/assets/c9349382-b712-4eaa-a278-e91d76d94678" />

## Chat Interface

<img width="1600" height="843" alt="Chat" src="https://github.com/user-attachments/assets/cba88d08-7590-4c66-84df-6aa72de8aac6" />

## Docker Images

<img width="1600" height="850" alt="Docker" src="https://github.com/user-attachments/assets/d880801f-349e-4990-a7d6-3ce68c6a3833" />


---

# Future Improvements

- Docker Compose Support
- Authentication System
- Redis Caching
- Hybrid Search (BM25 + Vector Search)
- Conversation Memory
- Streaming LLM Responses
- PDF Preview
- Citation-Based Answers
- Cloud Deployment

---

# What I Learned

While building this project, I explored:

- Production-style RAG pipelines
- Vector databases and semantic retrieval
- Event-driven backend workflows
- FastAPI architecture
- AI workflow orchestration
- Streamlit interactive applications
- Modular backend system design

---
