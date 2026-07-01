"""Shared LLM call (local Ollama). Written for you."""
import requests
from app.config import OLLAMA_URL, OLLAMA_MODEL


def call_llm(prompt, temperature=0.3):
    resp = requests.post(
        OLLAMA_URL,
        json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False,
              "options": {"temperature": temperature}},
        timeout=180,
    )
    resp.raise_for_status()
    return resp.json()["response"].strip()
