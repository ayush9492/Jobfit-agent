"""Layer 2: embed experience chunks + FAISS retrieval.

Plumbing written. YOU implement embed() and search().
"""
import argparse, json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from app.config import INDEX_PATH, CHUNKS_PATH, EMBED_MODEL, TOP_K

_model = None
def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBED_MODEL)
    return _model


def embed(texts):
    """
    TODO: return (N, D) float32 array of NORMALIZED embeddings for a list of strings.
    Hint: get_model().encode(texts, normalize_embeddings=True), cast to float32.
    Why normalized? lets us use inner-product search as cosine similarity.
    """
    raise NotImplementedError


def build_index():
    chunks = json.loads(CHUNKS_PATH.read_text())
    vecs = embed([c["text"] for c in chunks])
    index = faiss.IndexFlatIP(vecs.shape[1])
    index.add(vecs)
    faiss.write_index(index, str(INDEX_PATH))
    print(f"Indexed {index.ntotal} experience chunks.")


def search(query, k=TOP_K):
    """
    TODO: embed query, search FAISS, return top-k chunk dicts (+ score).
    Hint:
      chunks = json.loads(CHUNKS_PATH.read_text())
      index  = faiss.read_index(str(INDEX_PATH))
      s, idx = index.search(embed([query]), k)
      return [{**chunks[i], "score": float(sc)} for sc, i in zip(s[0], idx[0])]
    """
    raise NotImplementedError


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--build", action="store_true")
    if ap.parse_args().build:
        from app.experience import build_chunks
        build_chunks(); build_index()
