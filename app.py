import streamlit as st
from agent import review_code

st.set_page_config(page_title="CodeSentinel", layout="wide")
st.title("🛡️ CodeSentinel – Agentic Code Reviewer")
st.markdown("Paste your Python code. The AI agent will autonomously analyze structure, complexity, security, documentation, and retrieve best practices via hybrid RAG (BM25 + FAISS).")

code = st.text_area("📝 Python code to review:", height=300, placeholder="def hello():\n    print('world')")

if st.button("🔍 Review Code"):
    if code.strip():
        with st.spinner("Agent is analyzing your code (calling tools in optimal order)..."):
            report = review_code(code)
        st.subheader("📊 Review Report")
        st.markdown(report)
    else:
        st.warning("Please paste some Python code.")