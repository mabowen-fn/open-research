import os
import yaml
from openai import OpenAI  # Standard client, compatible with OpenClaw/OpenAI
from prompts import DRAFT_PROMPT, POLISH_PROMPT
from pypdf import PdfReader


def load_config():
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def read_local_papers(download_dir):
    """
    Simulated PDF parser for CLI pipeline. In a production OpenClaw env,
    you'd use PyPDF2 / pdfplumber or OpenClaw's native doc reader.
    """
    combined_content = ""
    if not os.path.exists(download_dir):
        return "No local papers found."

    files = [f for f in os.listdir(download_dir) if f.endswith(".pdf")]
    if not files:
        return "No PDF files available."

    print(f"📖 Processing {len(files)} downloaded papers for synthesis...")
    # For MVP demonstration, we pass the filenames and mock content metadata
    # Replace this block with your actual PDF text extractor
    for file in files:
        combined_content += f"\n--- Paper: {file} ---\n[Content extracted from {file} regarding methodology and results]\n"

    return combined_content


def run_agentic_pipeline():
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    client = OpenAI(
        api_key=config["openai_api_key"], base_url=config["openai_api_base"]
    )

    # 1. Real PDF ingestion
    raw_material = extract_text_from_pdfs(config["download_dir"])

    # Agent Step 1: Analytical Dissection
    print("\n🕵️‍♂️ [Agent 1/3] Analyst Agent is dissecting papers...")
    matrix_res = client.chat.completions.create(
        model=config["model_name"],
        messages=[{"role": "user", "content": ANALYST_AGENT.format(papers_content=raw_material)}],
        temperature=0.1,
    )
    matrix_content = matrix_res.choices[0].message.content

    # Agent Step 2: Synthesis & Structure
    print("✍️ [Agent 2/3] Writer Agent is constructing the narrative...")
    draft_res = client.chat.completions.create(
        model=config["model_name"],
        messages=[{"role": "user", "content": WRITER_AGENT.format(topic=config["search_query"], matrix_content=matrix_content)}],
        temperature=0.4,
    )
    draft_content = draft_res.choices[0].message.content

    # Agent Step 3: Peer-Review & Refinement Loop
    print("🔬 [Agent 3/3] Critic Agent is executing peer-review and rewriting...")
    final_res = client.chat.completions.create(
        model=config["model_name"],
        messages=[{"role": "user", "content": CRITIC_AGENT.format(draft_content=draft_content)}],
        temperature=0.2,
    )
    final_output = final_res.choices[0].message.content

    # Export output
    os.makedirs(config["output_dir"], exist_ok=True)
    out_file = os.path.join(config["output_dir"], "final_agentic_survey.md")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(final_output)

    print(f"\n🚀 System Complete! Agentic framework has outputted paper to: {out_file}")

def extract_text_from_pdfs(download_dir):
    """
    Scans the download directory, extracts text from downloaded PDFs,
    and structures them into manageable summaries for the context window.
    """
    if not os.path.exists(download_dir):
        return "No local papers found."

    pdf_files = [f for f in os.listdir(download_dir) if f.endswith(".pdf")]
    if not pdf_files:
        return "No PDF files available."

    print(f"📖 Deep parsing {len(pdf_files)} PDF manuscripts...")
    aggregated_context = ""

    for file_name in pdf_files:
        file_path = os.path.join(download_dir, file_name)
        try:
            reader = PdfReader(file_path)
            # Extract Abstract and Introduction (usually first 2 pages)
            # and Conclusion (usually last 1-2 pages) to stay efficient
            num_pages = len(reader.pages)

            extracted_text = f"\n=== START OF MANUSCRIPT: {file_name} ===\n"

            # Parse critical sections to optimize token limits
            for i in range(min(3, num_pages)):  # Front matter
                extracted_text += reader.pages[i].extract_text()

            if num_pages > 3:
                extracted_text += "\n[... Skipping Body Methodology ...]\n"
                for i in range(
                    max(num_pages - 2, 3), num_pages
                ):  # End/Conclusions
                    extracted_text += reader.pages[i].extract_text()

            extracted_text += f"\n=== END OF MANUSCRIPT: {file_name} ===\n"
            aggregated_context += extracted_text

        except Exception as e:
            print(f"⚠️ Warning: Could not parse {file_name}. Error: {e}")

    return aggregated_context

if __name__ == "__main__":
    run_agentic_pipeline
