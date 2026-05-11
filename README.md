# T&C AUTOS RAG Chatbot

AI-powered chatbot for T&C AUTOS, a Silicon Valley car dealership. Built with Groq API (free LLM), sentence-transformers (free embeddings), ChromaDB, and FastAPI.

**Zero monthly cost — $0 to run 24/7.**

## Architecture

```
User → HTML/CSS/JS Chat UI
          → FastAPI /chat
            → RAG Engine
              → ChromaDB (in-memory vector store)
              → sentence-transformers (free embeddings)
              → Groq API (free LLM, Llama 3 8B)
```

## Quick Start (Local)

```bash
pip install -r requirements.txt

# Generate synthetic data (if not already done)
python generate_synthetic_data.py

# Enrich inventory
python scripts/enrich_inventory.py

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open **http://localhost:8000**

## Deploy to Cloud (Free)

### Prerequisites

1. Sign up at **console.groq.com** → get a free API key (no credit card needed)
2. Push this repository to GitHub

### Deploy on Koyeb (Recommended — 24/7 always-on, free)

1. Sign up at **koyeb.com** (no credit card needed)
2. Create a new **App** → **Deploy from GitHub repository**
3. Select your repo, Koyeb auto-detects the `Dockerfile`
4. Add environment variable: `GROQ_API_KEY` = your Groq API key
5. Deploy — Koyeb builds and runs the container
6. Visit your app at `https://tcautos-chatbot-XXXX.koyeb.app`

### Deploy on Railway

1. Sign up at **railway.app**
2. New Project → **Deploy from GitHub repo**
3. Railway auto-detects the `Dockerfile`
4. Add `GROQ_API_KEY` as an environment variable
5. Deploy

## Project Structure

```
car_dealership/
├── app/
│   ├── main.py              # FastAPI server
│   ├── config.py            # Settings & API keys
│   └── rag_engine.py        # RAG pipeline
│   └── static/index.html    # Chat UI
├── knowledge_base/
│   ├── 01_company_info.md
│   ├── 02_services.md
│   ├── 03_promotions.md
│   ├── 04_financing.md
│   ├── 05_policies.md
│   ├── 06_faq.md
│   └── 07_inventory.md      # Auto-generated
├── scripts/
│   ├── enrich_inventory.py
│   └── ingest.py
├── data/                    # Synthetic CSV data
├── Dockerfile               # Container build
├── .dockerignore
└── requirements.txt
```

## API

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/chat` | Send message, get AI response |
| GET | `/` | Chat UI |

### POST /chat

```json
{
  "message": "What SUVs do you have under $40,000?",
  "history": []
}
```

Response:

```json
{
  "reply": "We have several great SUVs...",
  "sources": [
    { "source": "07_inventory.md", "relevance_score": 0.82 }
  ]
}
```

## Environment Variables

| Variable | Default | Required | Description |
|----------|---------|----------|-------------|
| `GROQ_API_KEY` | — | **Yes** | Groq API key (get from console.groq.com) |
| `LLM_MODEL` | `llama3-8b-8192` | No | Groq model to use |
| `EMBED_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | No | Embedding model |
| `RETRIEVAL_K` | `5` | No | Documents retrieved per query |

## Customization

- **Add knowledge**: Drop `.md` files into `knowledge_base/` and redeploy
- **Swap LLM**: Change `LLM_MODEL` to any Groq-supported model (e.g., `mixtral-8x7b-32768`, `gemma2-9b-it`)
