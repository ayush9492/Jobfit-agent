"""Central config. Know why each knob is set the way it is — interviewers ask."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXP_DIR = ROOT / "data" / "experience"
INDEX_PATH = ROOT / "data" / "faiss.index"
CHUNKS_PATH = ROOT / "data" / "chunks.json"

# Chunking — experience docs are short; smaller chunks keep each project distinct.
CHUNK_SIZE = 220       # words
CHUNK_OVERLAP = 40

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 5              # how many experience chunks to give the drafter

# Agent loop control — caps prevent infinite revise loops (a real agent concern).
MAX_REVISIONS = 2

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2"
