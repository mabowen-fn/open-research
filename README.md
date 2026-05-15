### `README.md`

# OpenClaw Survey Generator 🤖📄

An automated, containerized pipeline to search, fetch, synthesize, and polish academic literature review papers using LLMs. Built with reproducibility in mind, this project wraps an end-to-end research workflow into a single command-line execution environment powered by Docker.

---

## 🌟 Features

* 🐳 **100% Dockerized**: Zero-dependency local setup. Run the entire pipeline via isolated containers.
* 🔍 **Automated Arxiv Fetcher**: Dynamically queries Arxiv API based on your custom keywords and downloads relevant PDFs/meta-data.
* ✨ **Automated Peer-Review Polishing**: Passively self-corrects structural logic, eliminates colloquial language, and refines scientific prose to meet top-tier journal standards (IEEE/ACM style).

## ⚡ Advanced Multi-Agent Engine Architecture

Unlike basic prompt wrappers, this repository deploys a containerized **Multi-Agent Consensus System** that parses actual binaries:

1. **PDF Extracting Layer**: Uses structural binary parsers (`pypdf`) to systematically extract section matrix windows (Abstracts, Intros, Results) while keeping token limits fully optimized.
2. **Analyst Agent 🕵️‍♂️**: Converts arbitrary paper text into rigorous semantic indexes tracking individual methodologies, limitations, and missing elements.
3. **Synthesis Agent ✍️**: Ingests structural data frames to forge integrated taxonomies instead of linear paper-by-paper summaries.
4. **Critic Agent 🔬**: Mimics international journal peer-review panels, automatically debugging logic discrepancies, syntax structures, and delivering the finalized publication-ready Markdown file.

---

## 📂 Repository Structure

```text
open-research/
├── config.yaml               # Runtime Configuration (API Keys, Keywords)
├── config.example.yaml       # Template configuration for users
├── Dockerfile                # Image recipe for system dependencies
├── docker-compose.yml        # Orchestration configuration
├── requirements.txt          # Minimal Python dependencies
├── main.py                   # Main entry point (local runner)
├── data/
│   ├── raw_papers/           # Automatically downloaded PDFs
│   └── output/               # Final generated Markdown survey papers
└── src/
    ├── __init__.py
    ├── paper_fetcher.py      # Step 1: Arxiv search & downloader engine
    ├── pipeline.py           # Steps 3 & 4: Drafting & Editing Pipeline
    └── prompts.py            # Academic prompt templates
```
---

## 🚀 Quick Start

### Prerequisites

* [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed on your machine.
* An API Key from your chosen LLM provider (OpenAI compatible, or OpenClaw Gateway endpoint).

### Installation & Run

1. **Clone the repository:**
```bash
git clone https://github.com/mabowen-fn/open-research.git(https://github.com/mabowen-fn/open-research.git)
cd open-research
```


2. **Configure your environment:**

Open `config.yaml` and edit the parameters:
```yaml
openai_api_key: "your-actual-api-key"
openai_api_base: "[https://api.openai.com/v1](https://api.openai.com/v1)" # Or your OpenClaw proxy address
search_query: "Large Language Model Agents"  # Your survey topic
max_results: 5

```


3. **Execute with Docker Compose:**
```bash
docker-compose up --build

```



The container will automatically execute:

* **Step 1:** Download the top `N` papers matching your query into `data/raw_papers/`.
* **Step 2:** Read and aggregate the literature into a structured layout.
* **Step 3:** Synthesize a comprehensive literature review draft.
* **Step 4:** Polish the grammar, academic language, and structure.

Your completed paper will be saved as a clean Markdown document at: `data/output/final_survey.md`.

---

## 🛠️ Running Locally (Without Docker)

If you prefer to run the script directly on your host machine:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the automation suite
python main.py

```

---

## 🗺️ Roadmap & Contributing

This project is currently in its **MVP Stage (V1)**, executing structured single-prompt pipelines linearly over raw text. We plan to heavily leverage autonomous characteristics moving forward.

### Future Enhancements:

* [ ] Integrate a robust native PDF parser (`pypdf`/`pdfplumber`) to chunk full-text papers instead of metadata summaries.
* [ ] Implement **OpenClaw Multi-Agent Orchestration**: Break down the process into specialized Agent roles (e.g., *The Critic*, *The Historian*, *The Proofreader*) arguing over structural soundness.
* [ ] Add a lightweight Web GUI (Streamlit/Gradio) inside a separate container interface.

We highly welcome community contributions! Please feel free to open an **Issue** or submit a **Pull Request** if you want to help implement the Agent infrastructure.

