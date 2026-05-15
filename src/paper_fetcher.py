import os
import urllib.request
import xml.etree.ElementTree as ET
import yaml


def load_config():
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def fetch_arxiv_papers():
    config = load_config()
    query = config["search_query"].replace(" ", "+")
    max_results = config["max_results"]
    download_dir = config["download_dir"]

    os.makedirs(download_dir, exist_ok=True)

    # Arxiv API URL
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&max_results={max_results}&sortBy=relevance"

    print(f"🔍 Searching Arxiv for: '{config['search_query']}'...")

    try:
        response = urllib.request.urlopen(url)
        xml_data = response.read()
        root = ET.fromstring(xml_data)

        # Namespace for Arxiv Atom feed
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        entries = root.findall("atom:entry", ns)

        if not entries:
            print("❌ No papers found.")
            return

        print(f"📥 Found {len(entries)} papers. Starting download...")

        for i, entry in enumerate(entries):
            title = entry.find("atom:title", ns).text.strip().replace("\n", " ")
            # Clean title for filename
            clean_title = (
                "".join(c for c in title if c.isalnum() or c in "._- ").strip()[:50]
            )

            # Find PDF link
            pdf_url = ""
            for link in entry.findall("atom:link", ns):
                if link.attrib.get("title") == "pdf":
                    pdf_url = link.attrib.get("href")
                    break
                if "pdf" in link.attrib.get("href", ""):
                    pdf_url = link.attrib.get("href")

            if pdf_url:
                # Arxiv PDF links sometimes lack .pdf extension in API, append it if needed
                if not pdf_url.endswith(".pdf"):
                    pdf_url += ".pdf"

                filename = f"{download_dir}/{i+1}_{clean_title}.pdf"
                print(f"   [{i+1}/{len(entries)}] Downloading: {title[:60]}...")
                urllib.request.urlretrieve(pdf_url, filename)

        print("✅ All papers downloaded successfully.")

    except Exception as e:
        print(f"❌ Error fetching papers: {e}")


if __name__ == "__main__":
    fetch_arxiv_papers()
