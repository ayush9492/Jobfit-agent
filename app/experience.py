"""Layer 1: load YOUR experience docs (.md) and chunk them.

Loading is written. YOU implement chunking (same idea as any RAG ingest).
"""
import json
from app.config import EXP_DIR, CHUNKS_PATH, CHUNK_SIZE, CHUNK_OVERLAP


def load_docs():
    """Return list of (filename, text) for every .md in EXP_DIR."""
    docs = []
    for p in sorted(EXP_DIR.glob("*.md")):
        docs.append((p.name, p.read_text()))
    return docs


def chunk_text(text, source):
    words = text.split()
    step = CHUNK_SIZE - CHUNK_OVERLAP
    chunks = []
    for i in range(0, len(words), step):
        window = words[i:i + CHUNK_SIZE]
        chunk = " ".join(window).strip()
        if chunk:
            chunks.append({"text": chunk, "source": source})
    return chunks


def build_chunks():
    docs = load_docs()
    if not docs:
        raise SystemExit(f"No .md files in {EXP_DIR}. Add your real experience first.")
    chunks = []
    for name, text in docs:
        chunks.extend(chunk_text(text, name))
    CHUNKS_PATH.write_text(json.dumps(chunks, indent=2))
    print(f"Wrote {len(chunks)} chunks from {len(docs)} docs.")
    return chunks


if __name__ == "__main__":
    build_chunks()
