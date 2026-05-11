"""RAG engine: Groq LLM + sentence-transformers embeddings + ChromaDB."""

import sys
import gc
from pathlib import Path
from typing import List, Dict, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import app.config as config
import groq
import chromadb
from sentence_transformers import SentenceTransformer

try:
    from langdetect import detect as detect_lang
except Exception:
    detect_lang = None


SYSTEM_PROMPT = """You are Alex, a friendly and knowledgeable sales assistant at {company_name} in {city}, {state}.

Your role is to help potential customers learn about our vehicles, services, promotions, financing options, and company policies. Be warm, professional, and helpful. Always answer based on the provided context. If the answer is not in the context, politely say you don't have that information and offer to connect the customer with a team member.

When mentioning vehicles, include key details: make, model, year, price, mileage, and condition. When mentioning services, include pricing if available. Always invite the customer to visit our showroom or schedule a test drive or service appointment.

IMPORTANT: The customer is communicating in {language_name}. You MUST respond in {language_name}. Use the same language as the customer. Do NOT use English unless the customer wrote in English."""


def chunk_markdown(text: str, source: str, max_chars: int = 500) -> List[Dict]:
    chunks = []
    sections = text.split("\n## ")
    for section in sections:
        section = section.strip()
        if not section:
            continue
        if len(section) <= max_chars:
            chunks.append({"text": section, "source": source})
        else:
            parts = section.split("\n\n")
            current = ""
            for part in parts:
                part = part.strip()
                if not part:
                    continue
                if current and len(current) + len(part) + 1 > max_chars:
                    chunks.append({"text": current.strip(), "source": source})
                    current = part
                else:
                    current = current + "\n\n" + part if current else part
            if current.strip():
                chunks.append({"text": current.strip(), "source": source})
    return chunks


class RAGEngine:
    def __init__(self):
        self.embedders = {}
        self.current_agent = None
        self.chroma = chromadb.Client()
        self.collections = {}
        self.groq_client = groq.Groq(api_key=config.GROQ_API_KEY)

    def _load_embedder(self, agent_name: str) -> SentenceTransformer:
        if self.current_agent == agent_name and agent_name in self.embedders:
            return self.embedders[agent_name]

        old = self.current_agent
        if old and old in self.embedders:
            del self.embedders[old]
            gc.collect()

        agent_cfg = config.AGENTS[agent_name]
        print(f"Loading embedder for {agent_name}...")
        self.embedders[agent_name] = SentenceTransformer(agent_cfg["embed_model"])
        self.current_agent = agent_name
        print(f"Embedder for {agent_name} ready")
        return self.embedders[agent_name]

    def build_knowledge_base(self):
        kb_dir = config.KB_DIR
        all_chunks = []
        for md_file in sorted(kb_dir.glob("*.md")):
            text = md_file.read_text(encoding="utf-8")
            all_chunks.extend(chunk_markdown(text, md_file.name, config.CHUNK_SIZE))

        texts = [c["text"] for c in all_chunks]
        metadatas = [{"source": c["source"]} for c in all_chunks]
        ids = [f"chunk_{i}" for i in range(len(all_chunks))]

        for agent_name, agent_cfg in config.AGENTS.items():
            print(f"Building KB for {agent_name} ({agent_cfg['embed_model']})...")
            embedder = SentenceTransformer(agent_cfg["embed_model"])
            embeddings = embedder.encode(texts, show_progress_bar=True).tolist()
            del embedder
            gc.collect()

            collection = self.chroma.create_collection(agent_cfg["collection_name"])
            collection.add(
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas,
                ids=ids,
            )
            self.collections[agent_name] = collection
            print(f"  KB built: {len(all_chunks)} chunks")

        self._load_embedder(config.DEFAULT_AGENT)
        print(f"KB ready. Default agent: {config.DEFAULT_AGENT}")

    def retrieve(self, query: str, agent_name: str = None, k: int = None) -> List[Dict]:
        agent_name = agent_name or config.DEFAULT_AGENT
        k = k or config.RETRIEVAL_K
        embedder = self._load_embedder(agent_name)
        q_emb = embedder.encode([query]).tolist()
        collection = self.collections[agent_name]
        results = collection.query(
            query_embeddings=q_emb,
            n_results=k,
            include=["documents", "metadatas", "distances"],
        )
        docs = []
        for i in range(len(results["ids"][0])):
            docs.append({
                "text": results["documents"][0][i],
                "source": results["metadatas"][0][i]["source"],
                "score": round(1.0 - results["distances"][0][i], 4),
            })
        return docs

    @staticmethod
    def detect_language(text: str) -> str:
        if detect_lang is None:
            return "en"
        try:
            return detect_lang(text)
        except Exception:
            return "en"

    @staticmethod
    def resolve_language(question: str, preferred: str) -> str:
        lang_code = preferred.strip().lower()
        if lang_code == "auto" or lang_code not in config.SUPPORTED_LANGUAGES:
            detected = RAGEngine.detect_language(question)
            if detected in config.SUPPORTED_LANGUAGES:
                return detected
            return "en"
        return lang_code

    def answer(self, question: str, history: List[Dict] = None, language: str = "auto", agent: str = None) -> Dict:
        agent = agent or config.DEFAULT_AGENT
        lang_code = self.resolve_language(question, language)
        lang_name = config.SUPPORTED_LANGUAGES.get(lang_code, "English")

        retrieved = self.retrieve(question, agent_name=agent)

        context_parts = []
        sources = []
        for i, doc in enumerate(retrieved):
            context_parts.append(f"[Source {i+1}]: {doc['text']}")
            sources.append({
                "source": doc["source"],
                "relevance_score": doc["score"],
            })
        context = "\n\n---\n\n".join(context_parts)

        system = SYSTEM_PROMPT.format(
            company_name=config.COMPANY_NAME,
            city=config.COMPANY_CITY,
            state=config.COMPANY_STATE,
            language_name=lang_name,
        )

        messages = [{"role": "system", "content": system}]

        if history:
            for msg in history[-6:]:
                role = "user" if msg.get("role") == "user" else "assistant"
                messages.append({"role": role, "content": msg.get("content", "")})

        user_content = f"""**Context from our knowledge base:**
{context}

**Customer Question:** {question}

**Your Response:"""
        messages.append({"role": "user", "content": user_content})

        response = self.groq_client.chat.completions.create(
            model=config.LLM_MODEL,
            messages=messages,
            temperature=0.3,
            max_tokens=512,
        )

        return {
            "reply": response.choices[0].message.content.strip(),
            "sources": sources,
            "agent": agent,
            "agent_label": config.AGENTS[agent]["label"],
            "agent_speed": config.AGENTS[agent]["speed"],
            "agent_emoji": config.AGENTS[agent]["emoji"],
        }
