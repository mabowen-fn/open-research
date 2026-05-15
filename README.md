# open-research 🤖📚

`openresearch` is an autonomous, multi-container research engineering engine designed to automatically fetch, parse, index, synthesize, and compile publication-ready literature review surveys. 

By leveraging a serverless FAISS vector space and a cooperative Multi-Agent workflow, `openresearch` transforms dozens of raw academic PDF manuscripts into structured, peer-reviewed, camera-ready PDF and Markdown surveys with fully tracked BibTeX bibliographies.

Optimized to run out-of-the-box on high-context, ultra-affordable **MiniMax AI (海螺 AI)** infrastructure.

---

## ⚡ System Architecture & Agent Topology

Unlike basic single-prompt wrapper scripts, `openresearch` treats literature synthesis as a multi-stage software engineering pipeline:

1. **Ingestion Layer 📄**: Downloads relevant PDF files via the Arxiv API. In tandem, metadata fields are processed by the `CitationEngine` to generate static `.bib` databases.
2. **Semantic Context Layer (RAG) 🧠**: Parsed PDF text slices are chunked and embedded using an optimized `FAISS` vector index, bypassing token limitation bottlenecks.
3. **Analyst Agent 🕵️‍♂️**: Queries the vector store to break down every paper's specific methodology, parameters, and limitations into an organized analytical index matrix.
4. **Writer Agent ✍️**: Ingests the matrix to construct a cohesive thematic breakdown, mapping concepts instead of writing a disjointed list of summaries.
5. **Critic Agent 🔬**: Reviews the paper against top-tier journal standards (IEEE/ACM style) to remove colloquial phrases, repair logical breaks, and implement complex structural edits.
6. **Verification Agent 🛡️**: A deterministic gatekeeper that cross-checks citations inside the text against the tracked BibTeX keys to eliminate any potential LLM citation hallucinations.
7. **Compilation Layer 🖨️**: Pandoc intercepts the finalized Markdown, joins it with the `.bib` reference ledger, and outputs a publication-formatted PDF.

---

## 📂 Project Structure

```text
open-research/
├── config.yaml               # Runtime Configurations (MiniMax Base/Model settings)
├── config.example.yaml       # Template configuration file
├── Dockerfile                # System dependencies (Python, Pandoc, WeasyPrint)
├── docker-compose.yml        # Multi-Container orchestration matrix
├── requirements.txt          # Python packages (FAISS, Streamlit, Openai, pypdf)
├── main.py                   # Sequential backend script controller
├── gui/
│   └── app.py                # Streamlit Web Dashboard Frontend
├── data/
│   ├── raw_papers/           # Downloaded target PDF manuscripts
│   └── output/               # Final generated .md, .bib, and compiled .pdf documents
└── src/
    ├── __init__.py
    ├── paper_fetcher.py      # Arxiv retrieval engine
    ├── vector_store.py       # FAISS indexing & sliding-window RAG loader
    ├── citation_engine.py    # Deterministic BibTeX compiler & sanitizer
    ├── pipeline.py           # Core Multi-Agent orchestration logic
    └── prompts.py            # Academic persona prompts

```

---

## 🚀 Quick Start with Docker

### Prerequisites

* [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed.
* A API Key from the **MiniMax Developer Platform** (Mainland China or Global portal).

### 1. Setup Environment

Clone the repository and copy the environment template:

```bash
git clone [https://github.com/mabowen-fn/open-research.git](https://github.com/mabowen-fn/open-research.git)
cd open-research
```

### 2. Configure MiniMax Settings

Open `config.yaml` and enter your endpoint specifications:

```yaml
# LLM Provider Configuration
openai_api_key: "your-minimax-api-key-here"
openai_api_base: "[https://api.minimaxi.com/v1](https://api.minimaxi.com/v1)" # Use [https://api.minimax.io/v1](https://api.minimax.io/v1) for global accounts

# Choose your MiniMax Engine Tier
model_name: "MiniMax-M2.5"                     # 196K default context window (highly affordable)
# model_name: "MiniMax-M2.5-lightning"         # Use for 1M long-context scaling if processing 30+ papers

# Research Query Setup
search_query: "Reinforcement Learning from AI Feedback"
max_results: 8
download_dir: "./data/raw_papers"
output_dir: "./data/output"

```

### 3. Launch the System

Export your secret key to your shell environment and bring up the multi-container stack:

```bash
export MINIMAX_API_KEY="your_secret_key_here"
docker-compose up --build

```

---

## 🖥️ Interactive Web UI Dashboard

Once the containers are running, `openresearch` opens an interactive GUI on your host machine.

* Open your browser and navigate to **`http://localhost:8501`**
* Modify search queries, select your MiniMax model engine target, and adjust downloading thresholds inside the sidebar.
* Watch the live generation feed as the Analyst, Writer, and Critic agents communicate.
* One-click download your generated `.md` draft, your `.bib` bibliography index, or the compiled academic-formatted `.pdf` file.

---

## 🛠️ Running Locally (Without Docker)

If you have native Python environments configured and prefer direct execution:

1. **Install System Pre-requisites (Required for Document Compilation)**:
* **Linux**: `sudo apt install pandoc weasyprint`
* **macOS**: `brew install pandoc` + `pip install weasyprint`


2. **Install Python Packages**:
```bash
pip install -r requirements.txt

```


3. **Run Suite Run**:
```bash
python main.py

```



---

## 🗺️ Future Roadmap & Contributions

`openresearch` is actively maintained to help researchers optimize literature review pipelines. We welcome community PRs for the following targets:

* [ ] **Zotero & Mendeley Syncing**: Integration components to query local user library databases alongside Arxiv tracking.
* [ ] **Agentic Human-in-the-Loop Intersections**: Interface triggers allowing researchers to approve or reject the taxonomy outline *before* the Writer Agent generates the text body.
* [ ] **Custom LaTeX Style Templates**: Allowing users to upload custom `.sty` files directly via the Streamlit UI to match specific target conference templates (e.g., NeurIPS, CVPR, ACL).

