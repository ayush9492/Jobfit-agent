"""Layer 5: Streamlit UI — agent + ATS score + tailored resume download.

Flow:
  1. Paste a job description.
  2. Agent generates tailored bullets (retrieve → draft → critique → revise).
  3. Extract JD keywords, score the BASE resume vs the TAILORED resume (before/after).
  4. Download the full tailored resume as a PDF.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re
import streamlit as st

from app.agent import run
from app.scoring import extract_keywords, score
from app.resume_data import resume_to_text
from app.pdf_export import build_resume_pdf

st.set_page_config(page_title="JobFit Agent", page_icon="🎯", layout="wide")
st.title("JobFit Agent — tailored resume + ATS score")


def parse_bullets(text):
    """Pull '- ' style bullet lines out of the agent's raw output."""
    lines = []
    for ln in text.splitlines():
        ln = ln.strip()
        if ln.startswith(("- ", "* ", "• ")):
            lines.append(ln[2:].strip())
    # fallback: if the model didn't use dashes, take non-empty, non-preamble lines
    if not lines:
        for ln in text.splitlines():
            ln = ln.strip()
            if ln and not ln.lower().startswith("here"):
                lines.append(ln)
    return lines


jd = st.text_area("Paste a job description:", height=220)

if st.button("Tailor & Score") and jd.strip():
    with st.spinner("Running agent: retrieve → draft → critique → revise..."):
        result = run(jd)
    bullets_text = result["bullets"]
    bullets = parse_bullets(bullets_text)

    with st.spinner("Extracting keywords and scoring..."):
        keywords = extract_keywords(jd)
        resume_text = resume_to_text()
        result_score = score(resume_text, keywords)

    # ---- ATS match score + gap analysis ----
    st.subheader("ATS keyword match")
    c1, c2 = st.columns(2)
    c1.metric("Resume matches this JD", f"{result_score['score']}%")
    c2.metric("Keywords in JD", result_score["total"])

    st.markdown("**✅ Matched:** " + (", ".join(result_score["matched"]) or "—"))
    st.markdown("**❌ Missing:** " + (", ".join(result_score["missing"]) or "none 🎉"))
    st.caption("Missing = skills this JD asks for that aren't on your resume. "
               "If a missing keyword is genuinely true of your experience but worded "
               "differently, add the JD's exact term to resume_data.py (that honestly "
               "raises your match). If it's a real gap, it's something to learn — don't fake it.")
    # ---- tailored bullets ----
    st.subheader("Tailored bullets")
    for b in bullets:
        st.markdown(f"- {b}")
    st.caption(f"Revisions made: {result['revisions']} | Sources: {', '.join(result['sources'])}")

    # ---- download clean resume (1 page, no highlights section) ----
    pdf_bytes = build_resume_pdf()
    st.download_button(
        "⬇️ Download resume (PDF)",
        data=pdf_bytes,
        file_name="Ayush_Bharatiya_Resume.pdf",
        mime="application/pdf",
    )
    st.caption("The bullets above are draft suggestions for this role — review them and "
               "only use ones grounded in your real experience. The download is your clean "
               "one-page resume.")

    with st.expander("Agent trace (plan → draft → critique → revise)"):
        st.json(result["trace"])