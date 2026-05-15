import os
import yaml
from openai import OpenAI  # Standard client, compatible with OpenClaw/OpenAI
from prompts import DRAFT_PROMPT, POLISH_PROMPT


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


def run_pipeline():
    config = load_config()

    # Initialize Client
    client = OpenAI(
        api_key=config["openai_api_key"], base_url=config["openai_api_base"]
    )

    # 1. Gather Content
    papers_content = read_local_papers(config["download_dir"])

    # 2. Step 3: Generate Initial Survey Draft
    print("🤖 Step 3: Generating initial literature survey draft...")
    draft_response = client.chat.completions.create(
        model=config["model_name"],
        messages=[
            {
                "role": "user",
                "content": DRAFT_PROMPT.format(
                    topic=config["search_query"], papers_content=papers_content
                ),
            }
        ],
        temperature=0.3,
    )
    draft_text = draft_response.choices[0].message.content

    # 3. Step 4: Polish and Refine
    print("✨ Step 4: Polishing language and validating logic...")
    polished_response = client.chat.completions.create(
        model=config["model_name"],
        messages=[
            {
                "role": "user",
                "content": POLISH_PROMPT.format(draft_content=draft_text),
            }
        ],
        temperature=0.2,
    )
    final_survey = polished_response.choices[0].message.content

    # Save Output
    os.makedirs(config["output_dir"], exist_ok=True)
    output_path = f"{config['output_dir']}/final_survey.md"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_survey)

    print(f"🎉 Success! Final polished survey saved to: {output_path}")


if __name__ == "__main__":
    run_pipeline()
