"""Layer 5: Streamlit UI. Written for you. Shows the agent's revision trace —
great for screenshots in your portfolio."""
import streamlit as st
from app.agent import run

st.set_page_config(page_title="JobFit Agent", page_icon="🎯")
st.title("JobFit Agent — tailored, grounded resume bullets")

jd = st.text_area("Paste a job description:", height=200)
if st.button("Tailor") and jd.strip():
    with st.spinner("Retrieving experience → drafting → critiquing → revising..."):
        result = run(jd)
    st.markdown("### Bullets")
    st.write(result["bullets"])
    st.caption(f"Revisions made: {result['revisions']} | Sources: {', '.join(result['sources'])}")
    with st.expander("Agent trace (plan → draft → critique → revise)"):
        st.json(result["trace"])
