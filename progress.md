# T&C AUTOS RAG Chatbot — Progress Handoff

## Project Overview

AI-powered RAG chatbot for **T&C AUTOS**, a Silicon Valley car dealership. Built as a demo project for potential AI clients — shows how to build a production-ready RAG chatbot with synthetic data, free cloud deployment, and an automotive-themed UI.

**Goal:** 24/7 chatbot that answers customer questions about vehicles, services, promotions, financing, and company info.

---

## Current State (Completed)

### 1. Synthetic Data Generator
- **File:** `car_dealership/generate_synthetic_data.py`
- Generates 7 relational CSV files with realistic car dealership data
- Tables: dealerships (10), employees (80), customers (2,000), vehicles (500), sales (206), service records (3,000), leads (1,000)
- Run once with: `python generate_synthetic_data.py`

### 2. Knowledge Base Documents
- **Directory:** `car_dealership/knowledge_base/`
- 7 markdown files covering every domain a car dealership chatbot needs:

| File | Content | Lines |
|------|---------|-------|
| `01_company_info.md` | T&C AUTOS profile, Silicon Valley location, hours, team, mission | ~1.5KB |
| `02_services.md` | Full service menu with pricing (oil change $49.99, etc.), ASE-certified | ~3.5KB |
| `03_promotions.md` | May 2026 lease specials, 0% APR, trade-in bonus, referral program | ~2KB |
| `04_financing.md` | Loan/lease options, credit tiers (580+), extended warranty plans | ~2.5KB |
| `05_policies.md` | 7-day exchange, warranty info, trade-in policy, privacy | ~3KB |
| `06_faq.md` | 20+ Q&A about test drives, financing, service, purchasing | ~5.5KB |
| `07_inventory.md` | 500 vehicle listings auto-generated from CSV with rich descriptions | ~267KB |

### 3. Inventory Enrichment Script
- **File:** `car_dealership/scripts/enrich_inventory.py`
- Converts `vehicles.csv` → natural language markdown entries in `07_inventory.md`
- Each vehicle gets a structured listing with specs, price, and a descriptive sentence
- Already run — inventory document is populated

### 4. Multi-Language Support

- **12 languages** supported: English, French, Spanish, German, Dutch, Portuguese, Russian, Hindi, Bengali, Mandarin Chinese, Arabic, Urdu
- **UI:** Language selector dropdown in header (Auto Detect + 12 languages)
- **Detection:** `langdetect` library auto-detects user's language when set to "Auto Detect"
- **System prompt:** Dynamically injects `{language_name}` — instructs Alex to respond in the customer's language
- **Files changed:** `config.py`, `rag_engine.py`, `main.py`, `index.html`, `requirements.txt`

### 5. Dual-Agent System (Bob & June)

Two RAG agents with different embedding models sharing the same KB and LLM:

| Agent | Embedding Model | Size | Speed | Best For |
|-------|----------------|------|-------|----------|
| **June** (default) | `all-MiniLM-L6-v2` | ~80MB | Fast | English queries, low latency |
| **Bob** | `paraphrase-multilingual-MiniLM-L12-v2` | ~470MB | Slow | Multi-language queries (50+ langs) |

- **Architecture:** Single `RAGEngine` class manages both agents
- **Memory management:** Only one embedder loaded at a time. `_load_embedder()` swaps on-demand with `gc.collect()` — ~1-2s delay on first query after switching
- **KB builds:** Both collections (`bob_kb`, `june_kb`) built at startup sequentially. Each re-encodes the same chunks with its own embedder
- **UI:** Agent selector dropdown (June ⚡ Fast / Bob 🐢 Slow) in header. Speed badge on every assistant message bubble
- **API:** `agent` field in `ChatRequest`/`ChatResponse`
- **Config:** `config.AGENTS` dict with label, speed, emoji, color, collection name per agent

### 6. RAG Engine (v3 — Dual-Agent)
- **File:** `car_dealership/app/rag_engine.py`
- **Architecture:** No LangChain — uses raw SDKs for simplicity and control
- **Components:**
  - Two `SentenceTransformer` models (lazy-loaded, swapped on demand)
  - Two `chromadb.Client()` ephemeral in-memory collections
  - `groq.Groq()` API client with `llama3-8b-8192` (free tier)
  - Manual `chunk_markdown()` function (splits by `##` headers, then paragraphs, max 500 chars)
- **Pipeline:** `build_knowledge_base()` → embed with each agent → store in ChromaDB → `retrieve()` + `answer()` per query
- **Persona:** "Alex" — friendly sales assistant at T&C AUTOS
- **Memory:** Last 6 conversation turns maintained in request history (stateless API)

### 7. FastAPI Server
- **File:** `car_dealership/app/main.py`
- Endpoints:
  | Method | Path | Purpose |
  |--------|------|---------|
  | POST | `/chat` | `{message, history, language, agent}` → `{reply, sources, agent}` |
  | GET | `/health` | `{status: "ok", company: "T&C AUTOS"}` |
  | GET | `/` | Serves chat UI |
- Startup event builds both agent KBs automatically

### 8. Chat UI
- **File:** `car_dealership/app/static/index.html`
- Dark theme with automotive red accent (#e63946)
- Chat bubbles with typing indicator
- Source badges showing which knowledge base document was cited
- 5 suggested starter questions (SUVs under $40K, oil change price, lease specials, hours, first-time financing)
- Agent selector in header (June &#9889; Fast / Bob &#128422; Slow)
- Agent speed badge on each assistant message bubble
- Language selector with 12 languages + auto-detect
- Health check polling every 15s

### 9. Config
- **File:** `car_dealership/app/config.py`
- All settings via environment variables with sensible defaults
- Key vars: `GROQ_API_KEY` (required), `LLM_MODEL`, `EMBED_MODEL`, `RETRIEVAL_K`, `DEFAULT_AGENT`, `DEFAULT_LANGUAGE`
- `AGENTS` dict configures both agents (model, label, speed, emoji, color, collection name)

### 10. Deployment (Free, 24/7, $0/mo)
- **Option A — Hugging Face Spaces (LIVE):** Docker-based, free 16GB RAM, 2 vCPUs, 50GB storage. Pre-downloads models in Docker build. Listens on port 7860 (`PORT` env var). Sleeps after 48h inactive (wakes on request).
  - **Space:** `adedapo/car_dealership_chatbot` at https://huggingface.co/spaces/adedapo/car_dealership_chatbot
  - **GitHub sync:** `ramonesimone/car_dealership` — auto-deploys on push
  - **Secret:** `GROQ_API_KEY` set in HF Space Settings → Repository secrets
  - **Build:** Docker build ~15-20 min first time (PyTorch + models), cached after
- **Option B — Koyeb:** Dockerfile-based, 512MB RAM, always-on. Pre-downloads models in Docker build.
- **Files:** `Dockerfile`, `.dockerignore`
- **LLM:** Groq API — free tier: 30 req/min, 14,400 req/day (Llama 3 8B)
- **Embeddings:** Two models; only one loaded in memory at a time (lazy swap)
- **Vector DB:** Two ChromaDB ephemeral collections (`bob_kb`, `june_kb`) — rebuilt on each cold start (~15s)

### 11. Requirements
- **File:** `car_dealership/requirements.txt`
- `fastapi`, `uvicorn`, `groq`, `chromadb`, `sentence-transformers`, `pydantic`, `langdetect`, `python-dotenv`

### 12. README
- **File:** `car_dealership/README.md`
- Full setup instructions for local and cloud deployment

---

## Project File Map

```
C:\Users\HP\projects\car_dealership\
├── app\
│   ├── config.py              # Settings (env vars + dotenv, AGENTS map, SUPPORTED_LANGUAGES)
│   ├── main.py                # FastAPI server (3 routes, agent + language params)
│   ├── rag_engine.py          # Dual-agent RAG pipeline (Bob & June, lazy model loading)
│   └── static\
│       └── index.html         # Chat UI (agent selector, lang selector, speed badges, dark theme)
├── knowledge_base\
│   ├── 01_company_info.md     # T&C AUTOS company profile
│   ├── 02_services.md         # Service menu + pricing
│   ├── 03_promotions.md       # Current offers + specials
│   ├── 04_financing.md        # Loan/lease options
│   ├── 05_policies.md         # Warranty + returns + trade-in
│   ├── 06_faq.md              # 20+ Q&A pairs
│   └── 07_inventory.md        # 500 vehicle listings (auto-generated)
├── scripts\
│   ├── enrich_inventory.py    # CSV → markdown converter
│   └── ingest.py              # Local ChromaDB builder (for development)
├── data\                      # Synthetic CSV data (generated)
├── Dockerfile                 # Container build for Koyeb deployment
├── .dockerignore
├── vercel.json                # Vercel serverless config
├── .vercelignore              # Files excluded from Vercel bundle
├── .gitignore
├── .env                       # API key (gitignored)
├── generate_synthetic_data.py # Original data generator
├── requirements.txt
└── README.md
```

---

## Technical Decisions

| Decision | Rationale |
|----------|-----------|
| **No LangChain** | Overkill for this scale — direct SDK calls are faster, simpler, fewer dependencies |
| **Dual-agent design** | Two embedding models (June ~80MB Fast, Bob ~470MB Slow). Only one in memory at a time via lazy loading + gc. User picks via UI dropdown |
| **Groq API** | Free Llama 3 8B inference. 14K req/day free tier. OpenAI-compatible API |
| **ChromaDB in-memory** | Fits in 512MB Koyeb container. Rebuilt on deploy (~5s). No DB hosting cost |
| **Chunk at 500 chars by header** | Vehicle entries are self-contained. Headers create natural splits. Small chunks = precise retrieval |
| **Stateless API** | History passed in request body. Easier to scale, no server-side session management |

---

## Deployment Instructions

### Option A: Hugging Face Spaces (Live)

- **Space:** https://huggingface.co/spaces/adedapo/car_dealership_chatbot
- **URL:** https://adedapo-car-dealership-chatbot.hf.space
- **GitHub sync:** Push to `ramonesimone/car_dealership` → auto-deploys
- **Secret:** `GROQ_API_KEY` set in Settings → Repository secrets

To redeploy after changes: `git push origin master` (triggers HF build).

### Option B: Create a New Space

1. Go to https://huggingface.co/new-space
2. Set Space name
3. **SDK:** Select "Docker"
4. **Space type:** Free
5. Connect your GitHub repo
6. Add `GROQ_API_KEY` in Settings → Repository secrets

### Option B: Koyeb

1. Get a free Groq API key: https://console.groq.com
2. Push the repo to GitHub
3. Go to https://koyeb.com → New App → Deploy from GitHub
4. Add env var: `GROQ_API_KEY` = your key
5. Deploy → URL is ready in 2 minutes

---

## Known Limitations & Future Work

| Issue | Severity | Suggestion |
|-------|----------|------------|
| Knowledge base content is mostly synthetic (except inventory) | Medium | Replace with real T&C AUTOS info (actual address, real promotions, real service pricing) |
| No lead capture | Low | User opted out, but could be added: detect "I want to buy/test drive" intents → save to DB |
| ~~No multi-language support~~ | ~~Medium~~ | **Done** — 12 languages + auto-detect |
| In-memory ChromaDB = cold start on deploy | Low | ~15s rebuild (two collections). Could be optimized by pre-computing embeddings and loading from file |
| HF Spaces sleeps after 48h inactivity | Low | Free Spaces go to sleep. Wakes on first request (~30s cold start). Upgrade to paid for always-on |
| Vehicle inventory is synthetic | High | Replace `07_inventory.md` with real dealership inventory feed |
| No authentication | Medium | Add simple password or API key for production use |
| Groq free tier limits | Medium | 30 req/min, 14,400/day. Should upgrade to paid tier if traffic grows |
| No analytics | Low | Track which questions are asked most, which sources are cited |

---

## How to Run Locally

```powershell
# 1. Install deps
pip install -r requirements.txt

# 2. Generate synthetic data (if not done)
python generate_synthetic_data.py

# 3. Enrich inventory
python scripts\enrich_inventory.py

# 4. Start server (builds both agent KBs on startup ~15s)
$env:GROQ_API_KEY = "gsk_your_key_here"
uvicorn app.main:app --reload --host 0.0.0.0 --port ${PORT:-7860}

# 5. Open http://localhost:7860
#    Default agent: June (Fast, English-optimized)
#    Switch to Bob (Slow, multilingual) via header dropdown
```

---

## Configuration Reference

| Env Variable | Default | Required | Description |
|---|---|---|---|
| `GROQ_API_KEY` | — | **Yes** | Groq API key for LLM access |
| `LLM_MODEL` | `llama3-8b-8192` | No | Groq model for generation |
| `EMBED_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | No | SentenceTransformer model for embeddings |
| `CHUNK_SIZE` | `500` | No | Max characters per chunk |
| `RETRIEVAL_K` | `5` | No | Number of chunks retrieved per query |
| `DEFAULT_LANGUAGE` | `auto` | No | Default UI language (`auto`, `en`, `fr`, `es`, `de`, `nl`, `pt`, `ru`, `hi`, `bn`, `zh-cn`, `ar`, `ur`) |
| `DEFAULT_AGENT` | `june` | No | Default agent (`june` or `bob`) |

---

*Handoff prepared: May 11, 2026 — Session 2*
*Stack: Python 3.12, FastAPI, Groq API, sentence-transformers (multilingual), ChromaDB, HF Spaces*

## Session 2 — What Was Done

| Task | Status |
|------|--------|
| Multi-language support (12 languages + auto-detect via `langdetect`) | Done |
| Dual-agent system (Bob 🐢 Slow multilingual / June ⚡ Fast English) | Done |
| Lazy model loading — only one embedder in RAM at a time | Done |
| Language selector + agent selector in chat UI header | Done |
| Agent speed badges on assistant message bubbles | Done |
| `.env` file with `python-dotenv` auto-loading | Done |
| Git repo initialized + pushed to `ramonesimone/car_dealership` | Done |
| HF Space `adedapo/car_dealership_chatbot` created (GitHub sync) | Done |
| Vercel attempted — blocked by PyTorch bundle size (5GB > 500MB limit) | Blocked |

### Files Modified This Session

| File | Change |
|------|--------|
| `app/config.py` | Added `AGENTS` dict, `SUPPORTED_LANGUAGES` map, `DEFAULT_AGENT`, `DEFAULT_LANGUAGE`, `python-dotenv` |
| `app/rag_engine.py` | Dual-agent RAG engine, `_load_embedder()` lazy swap, `detect_language()`, `resolve_language()`, language in system prompt |
| `app/main.py` | `language` + `agent` fields in `ChatRequest`, `agent` in `ChatResponse` |
| `app/static/index.html` | Agent selector, language selector, speed badges on bubbles, CSS for both |
| `requirements.txt` | Added `langdetect`, `python-dotenv` |
| `Dockerfile` | Port changed to `$PORT` env var (HF Spaces uses 7860), both models pre-downloaded |
| `.gitignore` | Created with `.env`, `__pycache__/`, etc. |
| `.dockerignore` | Added `.env.txt` |
| `progress.md` | Updated throughout |

### Files Created This Session

| File | Purpose |
|------|---------|
| `vercel.json` | Vercel FastAPI config (unused — kept as reference) |
| `.vercelignore` | Vercel bundle excludes (unused — kept as reference) |

### Next Steps / High Priority

1. ~~**Check HF Space build** — verify the Docker build completes and the chatbot is accessible~~ **Done**
2. ~~**Replace synthetic inventory** — decided to keep synthetic for demo portfolio~~ **Skipped**
3. ~~**Authentication** — add password/API key before sharing publicly~~ **Pending**
4. **Koyeb** — try if HF Spaces free tier sleep policy is an issue

---

## Session 3 — What Was Done

| Task | Status |
|------|--------|
| HF Space build fixed and deployed | Done |
| YAML config header added to README.md (sdk: docker, app_port: 7860) | Done |
| Dockerfile fixed for HF Spaces (USER user, --chown=user) | Done |
| Groq model updated: llama3-8b-8192 → llama-3.1-8b-instant | Done |
| facts.json created — curated ground-truth dealership info | Done |
| 08_inventory_summary.md created — full inventory overview by make/model/price | Done |
| Injection protection (3 layers): hardened prompt, delimiter isolation, ground truth cross-reference | Done |
| Vehicle image previews via Pollinations.ai — premium aesthetic prompts | Done |
| vehicle_images.json generated (500 images, URLs only, ~15KB) | Done |
| enrich_inventory.py updated with Vehicle ID field for exact image matching | Done |
| Chat UI now renders image gallery when vehicles are mentioned | Done |

### Files Created This Session

| File | Purpose |
|------|---------|
| `app/facts.json` | Curated ground-truth facts injected into system prompt |
| `app/vehicle_images.json` | 500 Pollinations.ai premium image URLs |
| `knowledge_base/08_inventory_summary.md` | Full inventory summary by make/model/price |
| `scripts/generate_vehicle_images.py` | Generates image URLs from vehicles.csv |
| `scripts/inventory_summary.py` | Generates inventory summary from CSV |
| `scripts/test_injection.py` | Injection safety test suite |

### Files Modified This Session

| File | Change |
|------|--------|
| `app/rag_engine.py` | Loads facts.json + vehicle_images.json, hardened system prompt with safety rules, delimiter isolation, image matching in answer() |
| `app/main.py` | Added `images: list = []` to ChatResponse |
| `app/static/index.html` | Image gallery rendering in chat bubbles, CSS for gallery |
| `scripts/enrich_inventory.py` | Added Vehicle ID field for chunk→image matching |
| `README.md` | Added YAML header for HF Spaces config |
| `Dockerfile` | Fixed user permissions for HF Spaces |
| `app/config.py` | Updated LLM_MODEL to llama-3.1-8b-instant |
| `progress.md` | Updated throughout |
