"""Layer 4: FastAPI. Plumbing written — wires up the agent you implemented."""
from fastapi import FastAPI
from pydantic import BaseModel
from app.experience import build_chunks
from app.store import build_index
from app.agent import run

app = FastAPI(title="JobFit Agent")


class JD(BaseModel):
    job_description: str
    k: int = 5


@app.post("/reindex")
def reindex():
    build_chunks(); build_index()
    return {"status": "ok"}


@app.post("/tailor")
def tailor(j: JD):
    return run(j.job_description, k=j.k)


@app.get("/health")
def health():
    return {"status": "ok"}
