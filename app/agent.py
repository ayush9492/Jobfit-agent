"""Layer 3: THE AGENT. This is the core of the project and what interviewers probe.

The loop structure (run) is written so you can see the control flow. YOU implement
the three reasoning steps — draft, critique, revise — because being able to explain
*how the agent decides* is the whole point of putting "agentic" on your resume.

Control flow:
    retrieve experience  ->  draft  ->  critique  ->  (pass? stop : revise) -> critique ...
with a hard cap of MAX_REVISIONS so it can never loop forever.
"""
import json
from app.store import search
from app.llm import call_llm
from app.config import TOP_K, MAX_REVISIONS


def draft_bullets(job_description, experience_chunks):
    """
    TODO (you implement):
    Prompt the LLM to write 3-4 tailored resume bullets for `job_description`,
    using ONLY facts present in `experience_chunks`. Return the raw text.

    Build the prompt so it:
      - lists the retrieved experience chunks as the only allowed source material
      - tells the model NOT to invent tools, metrics, or projects not in the chunks
      - asks for impact-first bullets that echo keywords from the job description
    Hint: format chunks as "[1] (source) text" and instruct "use only [1..N]".
    """
    raise NotImplementedError


def critique(job_description, bullets, experience_chunks):
    """
    TODO (you implement):
    Ask the LLM to act as a STRICT critic and return JSON like:
        {"pass": true/false, "issues": ["...", "..."]}

    The critic checks each bullet for:
      1. GROUNDING — is every claim supported by the experience chunks? (most important)
      2. KEYWORD FIT — does it reflect the job description's requirements?
      3. QUALITY — impact-first, concrete, no fluff.

    Parse the JSON safely (strip code fences, json.loads in try/except). On parse
    failure, treat as not-pass so the agent revises rather than shipping garbage.
    Return a dict {"pass": bool, "issues": [str]}.
    """
    raise NotImplementedError


def revise(job_description, bullets, issues, experience_chunks):
    """
    TODO (you implement):
    Prompt the LLM to rewrite `bullets` fixing the critic's `issues`, still grounded
    ONLY in `experience_chunks`. Return revised text.
    """
    raise NotImplementedError


def run(job_description, k=TOP_K, max_revisions=MAX_REVISIONS):
    """The agent loop. Written for you — it orchestrates the steps you implement."""
    chunks = search(job_description, k=k)          # tool call: retrieve experience
    bullets = draft_bullets(job_description, chunks)
    trace = [{"step": "draft", "output": bullets}]

    for i in range(max_revisions):
        verdict = critique(job_description, bullets, chunks)
        trace.append({"step": "critique", "verdict": verdict})
        if verdict.get("pass"):
            break
        bullets = revise(job_description, bullets, verdict.get("issues", []), chunks)
        trace.append({"step": f"revise_{i+1}", "output": bullets})

    return {
        "bullets": bullets,
        "sources": sorted({c["source"] for c in chunks}),
        "revisions": sum(1 for t in trace if t["step"].startswith("revise")),
        "trace": trace,
    }


if __name__ == "__main__":
    import sys
    jd = " ".join(sys.argv[1:]) or "ML engineer with RAG and agent experience, Python, FastAPI."
    print(json.dumps(run(jd), indent=2))
