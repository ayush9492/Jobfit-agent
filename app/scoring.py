"""ATS-style keyword scoring.

Approach (explainable):
  1. Extract concrete skill/tool/requirement keywords from the job description
     (LLM extraction, with a built-in tech-vocabulary fallback if the LLM fails).
  2. Check which keywords appear in the resume text.
  3. Score = matched / total, and surface the MISSING keywords so you know exactly
     what to add.

This mirrors how basic ATS keyword filters work and is fully interpretable.
"""
import json
import re

try:
    from app.llm import call_llm
except Exception:  # allows importing this module without Ollama for testing
    call_llm = None


# Fallback vocabulary used if LLM extraction is unavailable or fails.
TECH_VOCAB = [
    "python", "c++", "c", "java", "sql", "mysql", "postgresql", "mongodb", "nosql",
    "pytorch", "tensorflow", "scikit-learn", "keras", "spark", "spark ml", "pandas",
    "numpy", "matplotlib", "seaborn", "power bi", "tableau",
    "machine learning", "deep learning", "computer vision", "nlp", "llm", "llms",
    "generative ai", "rag", "agents", "prompt engineering", "fine-tuning",
    "statistics", "statistical modeling", "time-series", "anomaly detection",
    "fastapi", "flask", "django", "rest api", "docker", "kubernetes", "aws", "gcp",
    "azure", "cloud", "mlflow", "dvc", "streamlit", "git", "ci/cd",
    "faiss", "vector database", "embeddings", "opencv", "yolov8", "iot", "telematics",
    "data pipeline", "etl", "data visualization", "analytics", "sqlalchemy", "pydantic",
]


def _parse_json_list(raw):
    """Pull a JSON array out of a possibly-messy LLM response."""
    cleaned = re.sub(r"```(json)?", "", raw).strip()
    m = re.search(r"\[.*\]", cleaned, re.DOTALL)
    if not m:
        return []
    try:
        data = json.loads(m.group(0))
        return [str(x).strip() for x in data if str(x).strip()]
    except Exception:
        return []


def _vocab_fallback(jd):
    jd_l = jd.lower()
    return [kw for kw in TECH_VOCAB if _kw_in_text(kw, jd_l)]


def _dedupe(keywords):
    seen, out = set(), []
    for kw in keywords:
        key = kw.lower()
        if key not in seen:
            seen.add(key)
            out.append(kw)
    return out


def _kw_in_text(keyword, text_lower):
    """Word-boundary match for short tokens, substring for multiword phrases."""
    kw = keyword.lower().strip()
    if not kw:
        return False
    # escape regex special chars (c++, ci/cd, etc.)
    esc = re.escape(kw)
    if " " in kw or "-" in kw or "/" in kw:
        return esc.replace(r"\ ", r"\s+") in text_lower or kw in text_lower
    # single token: require word boundaries so "r" / "go" don't over-match
    return re.search(rf"(?<![a-z0-9]){esc}(?![a-z0-9])", text_lower) is not None


def extract_keywords(jd, max_keywords=25):
    """Return a list of key skills/requirements from the job description."""
    keywords = []
    if call_llm is not None:
        prompt = (
            "Extract the key technical skills, tools, technologies, and hard requirements "
            "from this job description. Return ONLY a JSON array of short keyword strings "
            '(e.g. ["Python", "machine learning", "SQL", "Docker"]). Focus on concrete, '
            "checkable skills and tools, not soft skills or fluff.\n\n"
            f"JOB DESCRIPTION:\n{jd}\n\nJSON array:"
        )
        try:
            keywords = _parse_json_list(call_llm(prompt))
        except Exception:
            keywords = []
    if not keywords:
        keywords = _vocab_fallback(jd)
    return _dedupe(keywords)[:max_keywords]


def score(resume_text, keywords):
    """Score resume_text against a list of keywords. Returns dict with details."""
    rt = resume_text.lower()
    matched, missing = [], []
    for kw in keywords:
        (matched if _kw_in_text(kw, rt) else missing).append(kw)
    total = len(keywords)
    pct = round(100 * len(matched) / total) if total else 0
    return {"score": pct, "matched": matched, "missing": missing, "total": total}