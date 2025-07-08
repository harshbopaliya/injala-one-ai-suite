# app.py

import streamlit as st
from model_utils import load_gemini
from auto_router import detect_agent_with_gemini

# === Import all agents ===
from asuretify import AsuretifyAgent
from kinetic import KineticAgent
from wrappotal import WrappotalAgent
from riskguru import RiskguruAgent
from prequaligy import PrequaligyAgent
from anzenn import AnzennAgent

# === Agent Registry ===
AGENTS = {
    "asuretify": {"class": AsuretifyAgent, "file_count": 2},
    "kinetic": {"class": KineticAgent, "file_count": 1},
    "wrappotal": {"class": WrappotalAgent, "file_count": 1},
    "riskguru": {"class": RiskguruAgent, "file_count": 1},
    "prequaligy": {"class": PrequaligyAgent, "file_count": 1},
    "anzenn": {"class": AnzennAgent, "file_count": 1},
}

# === UI Layout ===
st.set_page_config(page_title="Injala One AI Suite", layout="centered")
st.title("🤖 Injala One AI Agent Suite")
st.markdown(
    "Upload 1–2 PDFs and ask a question. The system will auto-select the best AI agent "
    "to analyze your documents and return a structured report."
)

# === Ask for Gemini API Key explicitly ===
api_key = st.text_input(
    "🔑 Enter your Gemini API Key",
    type="password",
    placeholder="Paste your Gemini API key here to proceed"
)

if not api_key:
    st.warning("⚠️ Please enter your Gemini API key to proceed.")
    st.stop()

# === Load LLM Model ===
try:
    model = load_gemini(api_key)
except Exception as e:
    st.error(f"❌ Failed to initialize Gemini model:\n\n{e}")
    st.stop()

# === User Input ===
query = st.text_area(
    "📝 Your Query",
    placeholder="e.g., Compare contract vs COI for insurance compliance"
)
files = st.file_uploader(
    "📎 Upload PDF(s)",
    type=["pdf"],
    accept_multiple_files=True
)

# === Execution Trigger ===
if query and files:
    with st.spinner("🔍 Analyzing input and selecting the best agent..."):
        try:
            # Auto-detect agent and file mapping
            agent_key, file_idxs = detect_agent_with_gemini(model, query, files)

            if agent_key not in AGENTS:
                st.error(f"❌ No matching agent found for: `{agent_key}`")
                st.stop()

            agent_info = AGENTS[agent_key]
            required_files = agent_info["file_count"]

            if len(file_idxs) != required_files:
                st.error(f"❌ Agent `{agent_key}` needs {required_files} file(s), but got {len(file_idxs)}.")
                st.stop()

            # Read files
            file_bytes = [files[i].read() for i in file_idxs]

            # Run agent
            agent = agent_info["class"](model)
            result = agent.run(*file_bytes)

            # Output result
            st.subheader("📋 Agent Response")
            st.text_area("📄 Output", result, height=400)

            # Optional download button for structured output
            st.download_button(
                "📥 Download Result",
                result.encode(),
                "agent_output.txt",
                "text/plain"
            )

        except Exception as e:
            st.error("⚠️ Error occurred during processing:")
            st.exception(e)
else:
    st.info("💡 Please enter a query and upload 1–2 PDFs to begin.")
