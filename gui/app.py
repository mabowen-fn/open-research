# gui/app.py
import streamlit as st
import os
import yaml
import subprocess

st.set_page_config(page_title="OpenClaw Survey Agent", page_icon="📝", layout="wide")

st.title("🤖 OpenClaw Automated Academic Survey Generator")
st.subheader("Generate publication-ready literature reviews using a Multi-Agent pipeline.")

col1, col2 = st.columns(2)

pdf_file_path = "data/output/academic_review.pdf"
md_file_path = "data/output/final_survey.md"

with col1:
    if os.path.exists(md_file_path):
        with open(md_file_path, "r", encoding="utf-8") as f:
            st.download_button("📥 Download Markdown Version", f.read(), "paper.md", "text/markdown")

with col2:
    if os.path.exists(pdf_file_path):
        with open(pdf_file_path, "rb") as f:
            st.download_button("📥 Download Compiled Academic PDF", f.read(), "academic_review.pdf", "application/pdf")

# Sidebar Configuration
st.sidebar.header("⚙️ Configuration")
query = st.sidebar.text_input("Research Topic / Search Query", "Large Language Model Agents")
max_papers = st.sidebar.slider("Number of Arxiv Papers to Fetch", 3, 20, 5)
model = st.sidebar.selectbox("LLM Model Engine", ["gpt-4o", "gpt-3.5-turbo", "claude-3-opus"])

if st.sidebar.button("🚀 Launch Agentic Pipeline"):
    # Dynamically rewrite config.yaml based on UI inputs
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    config["search_query"] = query
    config["max_results"] = max_papers
    config["model_name"] = model
    
    with open("config.yaml", "w") as f:
        yaml.safe_dump(config, f)
        
    st.info("🔄 Running pipeline... Pulling items from Arxiv and initializing Agents.")
    
    # Run pipeline via sub-process or direct python import
    with st.spinner("Agents are analyzing, synthesizing, and peer-reviewing... Please wait."):
        result = subprocess.run(["python", "main.py"], capture_output=True, text=True)
        
    if result.returncode == 0:
        st.success("🎉 Process Complete!")
    else:
        st.error(f"Error executing pipeline: {result.stderr}")

# Display generated output
st.header("📄 Generated Output")
output_path = "data/output/final_agentic_survey.md"
if os.path.exists(output_path):
    with open(output_path, "r", encoding="utf-8") as f:
        survey_md = f.read()
    st.download_button("📥 Download Survey Paper (.md)", survey_md, file_name="literature_review.md")
    st.markdown(survey_md)
else:
    st.warning("No survey generated yet. Set parameters in the sidebar and click launch!")
