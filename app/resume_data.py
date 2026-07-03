"""Your base resume as structured data.

Used two ways:
  - resume_to_text() -> flat text for ATS keyword scoring
  - pdf_export.build_resume_pdf() -> renders this to a PDF

Keep this truthful and in sync with your real resume. Edit here when your
experience changes.
"""

RESUME = {
    "name": "AYUSH BHARATIYA",
    "contact": "ayushbharatiya@gmail.com | +1 (312) 358-2770 | Chicago, IL | "
               "linkedin.com/in/ayush-bharatiya-78a080202 | github.com/ayush9492",
    "summary": (
        "Product-minded Machine Learning Engineer with 2 years of experience shipping "
        "production systems end to end — models, APIs, and data pipelines — across finance "
        "and computer vision. Cut manual stock review ~70%, deployed an ANPR system "
        "processing >10,000 vehicle records/day, and build agentic LLM/RAG systems with "
        "FastAPI, Docker, and FAISS. M.S. in CS expected May 2027; available for summer "
        "2026 internships and 2027 new-grad roles."
    ),
    "education": [
        {"school": "Illinois Institute of Technology", "loc": "Chicago, IL",
         "detail": "M.S. in Computer Science | GPA: 3.50/4.0 | Aug 2025 – May 2027 (expected)"},
        {"school": "Gujarat Technological University", "loc": "Surat, GJ",
         "detail": "B.E. in Computer Science & Engineering (Minors: AI & ML) | GPA: 3.54/4.0 | Jun 2020 – Jun 2024"},
    ],
    "skills": [
        ("Machine Learning & AI", "PyTorch, TensorFlow, scikit-learn, Spark ML, LLMs (RAG, agents), MLflow"),
        ("Programming", "Python, C/C++, SQL"),
        ("Backend & Deployment", "FastAPI, Flask, Docker, REST API, Pydantic, DVC, Streamlit"),
        ("Data & Databases", "pandas, NumPy, FAISS, SQL, MySQL, MongoDB, SQLAlchemy, Power BI, Matplotlib, Seaborn, Git"),
    ],
    "experience": [
        {
            "org": "Triumph Capital", "loc": "Surat, GJ",
            "role": "Machine Learning Engineer & Data Analyst | Aug 2024 – Jul 2025",
            "bullets": [
                "Cut manual stock-screening time ~70% by building automated scanning algorithms in "
                "Python (pandas, NumPy) with statistical indicators (Relative Strength, ADX) and a "
                "custom backtesting framework.",
                "Engineered end-to-end pipelines ingesting >5M rows of market data via yfinance into "
                "SQL Server with vectorized pandas/NumPy cleansing; added batch scheduling and "
                "rate-limit controls to improve data freshness from daily to hourly.",
                "Reduced portfolio-manager decision latency ~40% by deploying a Streamlit + Power BI "
                "dashboard that let analysts filter stocks against custom statistical thresholds.",
            ],
        },
        {
            "org": "MyCiti 360 Technology Services", "loc": "Surat, GJ",
            "role": "Machine Learning Engineer & Data Analyst | Jan 2024 – Jul 2024",
            "bullets": [
                "Boosted identification accuracy ~25% across three sites by building ANPR and "
                "person-detection pipelines with TensorFlow and OpenCV plus Python-based unique-ID tracking.",
                "Cut incident response time ~30% with a real-time Flask + Power BI analytics dashboard "
                "ingesting >10K vehicle telemetry records/day from MySQL.",
            ],
        },
    ],
    "projects": [
        {
            "name": "JobFit Agent — Agentic Resume-Tailoring System",
            "stack": "Python, FastAPI, FAISS, Ollama (local LLM), Streamlit",
            "bullets": [
                "Built an agentic LLM system that tailors resume bullets to a job description via a "
                "retrieve → draft → critique → revise loop, using FAISS semantic search over an "
                "experience corpus and a locally-hosted LLM, served through FastAPI with a Streamlit UI.",
                "Designed a self-critique agent that grades each draft for factual grounding against "
                "retrieved chunks and triggers revision until it passes or hits a cap, with defensive "
                "JSON parsing for unreliable model output.",
                "Enforced a hallucination guardrail constraining generation to retrieved experience only; "
                "verified with a groundedness eval harness (100% grounded output, avg 0.7 revisions to "
                "converge) and confirmed the agent refuses to fabricate absent skills.",
            ],
        },
        {
            "name": "QuantaHealth — Quantum-Accelerated Drug Interaction Checker",
            "stack": "PennyLane, PyTorch, RDKit, MLflow, DVC, Docker, FastAPI, Streamlit",
            "bullets": [
                "Built a hybrid quantum-classical classifier predicting drug-interaction severity over "
                "240K labeled pairs (DDInter 2.0), using an 8-qubit PennyLane variational circuit feeding "
                "a PyTorch head over RDKit fingerprints; benchmarked against a classical baseline.",
                "Tracked all experiments in MLflow (model registry, A/B routing, one-click rollback) and "
                "versioned datasets with DVC; deployed end-to-end as a Dockerized FastAPI service with a "
                "Streamlit dashboard.",
            ],
        },
        {
            "name": "Real-Time Object Detection and Monitoring System",
            "stack": "YOLOv8, FastAPI, WebSockets, Docker Compose, Streamlit",
            "bullets": [
                "Real-time detection API (YOLOv8 + FastAPI, WebSocket streaming) in Docker Compose, with "
                "a Streamlit dashboard for live bounding-box visualization, analytics, and alerting.",
            ],
        },
    ],
    "leadership": [
        "Hackathon Team Lead, Azadi ka Amrut Mahotsav SSIP (2022–23): led 5 to build a Whisper-based "
        "ASR prototype (WER <15%); finalist among 1,000+ teams.",
        "Core Team, Google Developer Student Club (2021–23): ran 8 Python/C/C++ workshops for 120+ students.",
    ],
}


def resume_to_text(resume=RESUME):
    """Flatten the resume into plain text for keyword scoring."""
    parts = [resume["name"], resume["contact"], resume["summary"]]
    for e in resume["education"]:
        parts += [e["school"], e["loc"], e["detail"]]
    for label, items in resume["skills"]:
        parts.append(f"{label}: {items}")
    for job in resume["experience"]:
        parts += [job["org"], job["role"]] + job["bullets"]
    for p in resume["projects"]:
        parts += [p["name"], p["stack"]] + p["bullets"]
    parts += resume["leadership"]
    return "\n".join(parts)