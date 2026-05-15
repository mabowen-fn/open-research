# src/citation_engine.py
import re
import os
import xml.etree.ElementTree as ET
import urllib.request

class CitationEngine:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.bib_entries = {}

    def generate_bibtex(self, arxiv_id, title, authors, year):
        """Generates a clean BibTeX entry and returns its citation key."""
        # Create a unique key: e.g., AuthorYearTitleKeywords
        first_author = authors[0].split()[-1].lower() if authors else "unknown"
        clean_title_word = re.sub(r'[^a-zA-Z]', '', title.split()[0].lower())
        citation_key = f"{first_author}{year}{clean_title_word}"
        
        authors_formatted = " and ".join(authors)
        
        bib_entry = f"""@article{{{citation_key},
  title={{{title}}},
  author={{{authors_formatted}}},
  journal={{arXiv preprint arXiv:{arxiv_id}}},
  year={{{year}}}
}}
"""
        self.bib_entries[citation_key] = bib_entry
        return citation_key

    def save_bib_file(self):
        """Writes all tracked references to a single bibliography file."""
        os.makedirs(self.output_dir, exist_ok=True)
        bib_path = os.path.join(self.output_dir, "references.bib")
        with open(bib_path, "w", encoding="utf-8") as f:
            for entry in self.bib_entries.values():
                f.write(entry + "\n")
        print(f"📚 Generated BibTeX database saved to: {bib_path}")
