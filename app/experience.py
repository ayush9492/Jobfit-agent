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
    """
    TODO (you implement):
    Sliding-window chunker. Split `text` into ~CHUNK_SIZE-word chunks with
    CHUNK_OVERLAP words of overlap. Return list of {"text":..., "source":...}.

    Hints:
      words = text.split()
      step = CHUNK_SIZE - CHUNK_OVERLAP
      for i in range(0, len(words), step): chunk = " ".join(words[i:i+CHUNK_SIZE])
      skip empty chunks
    """
    raise NotImplementedError("Implement chunk_text.")


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
