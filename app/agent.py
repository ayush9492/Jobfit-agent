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
    context = "\n".join(
        f"[{i+1}] (source: {c['source']}) {c['text']}"
        for i, c in enumerate(experience_chunks)
    )
    prompt = f"""You are helping tailor resume bullets for a job.

EXPERIENCE (the ONLY facts you may use):
{context}

JOB DESCRIPTION:
{job_description}

Write 3-4 resume bullets tailored to this job. Rules:
- Use ONLY facts found in the EXPERIENCE above. Do NOT invent tools, metrics, or projects.
- Lead with impact/outcome where a metric exists in the experience.
- Echo relevant keywords from the job description where truthful.
- One bullet per line, starting with "- ".
"""
    return call_llm(prompt)


def critique(job_description, bullets, experience_chunks):
    context = "\n".join(
        f"[{i+1}] (source: {c['source']}) {c['text']}"
        for i, c in enumerate(experience_chunks)
    )
    prompt = f"""You are a STRICT resume critic. Check the bullets below.

EXPERIENCE (the only allowed source of facts):
{context}

JOB DESCRIPTION:
{job_description}

BULLETS TO CHECK:
{bullets}

Check ONLY for clear fabrication: a tool, metric, company, or project that does NOT
appear anywhere in the EXPERIENCE above. If every claim traces to the experience,
return pass: true. Do NOT flag bullets that are accurate but could be worded better.
When unsure, pass.

Respond ONLY with JSON, no other text:
{{"pass": true or false, "issues": ["issue 1", "issue 2"]}}
"""
    raw = call_llm(prompt)
    import json, re
    cleaned = re.sub(r"```(json)?", "", raw).strip()
    try:
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        result = json.loads(match.group(0)) if match else {}
        return {"pass": bool(result.get("pass", False)),
                "issues": result.get("issues", [])}
    except Exception:
        return {"pass": False, "issues": ["Could not parse critic response."]}


def revise(job_description, bullets, issues, experience_chunks):
    context = "\n".join(
        f"[{i+1}] (source: {c['source']}) {c['text']}"
        for i, c in enumerate(experience_chunks)
    )
    issue_list = "\n".join(f"- {x}" for x in issues)
    prompt = f"""Revise these resume bullets to fix the listed issues.

EXPERIENCE (the ONLY facts you may use):
{context}

JOB DESCRIPTION:
{job_description}

CURRENT BULLETS:
{bullets}

ISSUES TO FIX:
{issue_list}

Rewrite the bullets fixing every issue. Use ONLY facts from EXPERIENCE.
One bullet per line, starting with "- ". Respond with only the bullets.
"""
    return call_llm(prompt)


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
