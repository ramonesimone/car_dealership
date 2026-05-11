"""Chunk, embed, and store knowledge base documents into ChromaDB (local use)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import app.config as config
import chromadb
from sentence_transformers import SentenceTransformer
from app.rag_engine import chunk_markdown


def main():
    kb_dir = config.KB_DIR
    if not kb_dir.exists():
        print(f"Error: {kb_dir} does not exist.")
        sys.exit(1)

    print("Loading documents...")
    all_chunks = []
    for md_file in sorted(kb_dir.glob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        chunks = chunk_markdown(text, md_file.name, config.CHUNK_SIZE)
        all_chunks.extend(chunks)
        print(f"  {md_file.name}: {len(chunks)} chunks")

    print(f"Total: {len(all_chunks)} chunks")

    print("Loading embedding model...")
    embedder = SentenceTransformer(config.EMBED_MODEL)

    print("Computing embeddings...")
    texts = [c["text"] for c in all_chunks]
    embeddings = embedder.encode(texts, show_progress_bar=True).tolist()

    print("Storing in ChromaDB...")
    chroma_dir = config.BASE_DIR / "chroma_db"
    chroma_client = chromadb.PersistentClient(path=str(chroma_dir))
    collection = chroma_client.create_collection("tcautos_kb")

    metadatas = [{"source": c["source"]} for c in all_chunks]
    ids = [f"chunk_{i}" for i in range(len(all_chunks))]
    collection.add(
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas,
        ids=ids,
    )

    print(f"\nDone! Stored {len(all_chunks)} chunks in {chroma_dir}")


if __name__ == "__main__":
    main()
