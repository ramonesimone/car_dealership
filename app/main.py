"""FastAPI server for T&C AUTOS RAG Chatbot."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional

from app.rag_engine import RAGEngine

app = FastAPI(title="T&C AUTOS Chatbot")
engine = None


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[dict]] = None
    language: Optional[str] = "auto"
    agent: Optional[str] = "june"


class ChatResponse(BaseModel):
    reply: str
    sources: list
    images: list = []
    agent: str


@app.on_event("startup")
def startup():
    global engine
    engine = RAGEngine()
    engine.build_knowledge_base()


@app.get("/health")
def health():
    return {"status": "ok", "company": "T&C AUTOS"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    result = engine.answer(req.message, req.history, req.language, req.agent)
    return ChatResponse(reply=result["reply"], sources=result["sources"], images=result.get("images", []), agent=result["agent"])


STATIC_DIR = Path(__file__).resolve().parent / "static"
if STATIC_DIR.exists():
    app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")


@app.get("/")
def index():
    return FileResponse(str(STATIC_DIR / "index.html"))
