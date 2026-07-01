# JobFit Agent — agentic resume-bullet tailoring

Given a job description, an agent retrieves your *real* experience, drafts tailored
resume bullets, **critiques its own draft for honesty + keyword fit, and revises** —
looping until the critic passes or a max-iteration cap is hit.

The critic's #1 job: reject any bullet that isn't grounded in your real experience
corpus. The system is built so it *can't* fabricate — that's a feature you can talk
about in interviews.

Fully local, $0 stack:
- **LLM:** Ollama (e.g. `llama3.2`)
- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2`
- **Retrieval:** FAISS over your own experience docs
- **API:** FastAPI  **UI:** Streamlit

---

## Why this is "agentic" (your interview answer)

A plain RAG app does one pass: retrieve → answer. This does a **multi-step loop with
a control flow**: plan → retrieve → draft → critique → decide(revise or stop). The
agent makes a *decision* each turn (is this good enough?) instead of running a fixed
pipeline. That decision + loop is what makes it an agent, not just a chatbot.

```
job description
      │
      ▼
 ┌─────────┐   retrieve relevant experience (RAG over YOUR docs)
 │  PLAN   │──────────────┐
 └─────────┘              ▼
      ▲             ┌────────────┐
      │             │   DRAFT    │  tailored bullets
      │             └────────────┘
      │                   │
      │                   ▼
      │             ┌────────────┐  grounded? keyword fit? honest?
 revise if fail ────│  CRITIQUE  │
                    └────────────┘
                          │ pass
                          ▼
                     final bullets
```

---

## The build, in layers (you implement the TODOs)

1. **`app/experience.py`** — load + chunk YOUR experience docs from `data/experience/`.
2. **`app/store.py`** — embed chunks, FAISS search to retrieve experience for a JD.
3. **`app/agent.py`** — the loop: `plan` → `draft` → `critique` → `revise`. **The core.**
4. **`app/main.py`** / **`app/ui.py`** — API + UI (plumbing written for you).
5. **`eval/run_eval.py`** — measure groundedness: does every output bullet trace to a
   retrieved experience chunk? (Your standout, honesty-as-a-metric bullet.)

---

## Setup

```bash
ollama pull llama3.2
python -m venv .venv && source .venv/bin/activate   # Win: .venv\Scripts\activate
pip install -r requirements.txt

# Put YOUR real experience in data/experience/ as .md files —
# one per project/role, written honestly. (See data/experience/EXAMPLE.md)

python -m app.store --build           # after you implement experience.py + store.py
uvicorn app.main:app --reload         # http://localhost:8000/docs
streamlit run app/ui.py               # http://localhost:8501
```

## The honesty guardrail

The critic checks each drafted bullet against the retrieved chunks. If a bullet
claims something not supported by your experience corpus, the critic flags it and the
agent must revise or drop it. Keep `data/experience/` strictly truthful and the whole
system stays truthful by construction.
