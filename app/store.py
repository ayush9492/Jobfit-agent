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
    model = get_model()
    vecs = model.encode(texts, normalize_embeddings=True)
    return np.asarray(vecs, dtype="float32")


def build_index():
    chunks = json.loads(CHUNKS_PATH.read_text())
    vecs = embed([c["text"] for c in chunks])
    index = faiss.IndexFlatIP(vecs.shape[1])
    index.add(vecs)
    faiss.write_index(index, str(INDEX_PATH))
    print(f"Indexed {index.ntotal} experience chunks.")


def search(query, k=TOP_K):
    chunks = json.loads(CHUNKS_PATH.read_text())
    index = faiss.read_index(str(INDEX_PATH))
    qvec = embed([query])
    scores, idxs = index.search(qvec, k)
    return [{**chunks[i], "score": float(s)} for s, i in zip(scores[0], idxs[0])]


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--build", action="store_true")
    if ap.parse_args().build:
        from app.experience import build_chunks
        build_chunks(); build_index()
