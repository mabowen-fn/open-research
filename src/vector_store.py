# src/vector_store.py
import os
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class PaperRetriever:
    def __init__(self, download_dir):
        self.download_dir = download_dir
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.chunks = []

    def build_index(self):
        """Extracts text from all PDFs, chunks them, and builds a FAISS vector index."""
        if not os.path.exists(self.download_dir):
            return
        
        pdf_files = [f for f in os.listdir(self.download_dir) if f.endswith('.pdf')]
        raw_text_chunks = []
        
        print("🧠 Vectorizing papers for semantic Retrieval-Augmented Generation (RAG)...")
        for file_name in pdf_files:
            file_path = os.path.join(self.download_dir, file_name)
            try:
                reader = PdfReader(file_path)
                for page_num, page in enumerate(reader.pages):
                    text = page.extract_text()
                    # Basic sliding window chunking
                    words = text.split()
                    for i in range(0, len(words), 150):
                        chunk = " ".join(words[i:i+200])
                        if len(chunk.strip()) > 50:
                            # Attach source metadata to prevent hallucinations
                            self.chunks.append(f"[{file_name}, Page {page_num+1}]: {chunk}")
            except Exception as e:
                print(f"⚠️ Vectorizer skipped {file_name}: {e}")

        if not self.chunks:
            return

        # Generate embeddings and initialize FAISS
        embeddings = self.model.encode(self.chunks, show_progress_bar=False)
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings).astype('float32'))
        print(f"✅ Successfully indexed {len(self.chunks)} semantic chunks from {len(pdf_files)} papers.")

    def retrieve_relevant_context(self, query, k=8):
        """Finds the top K most contextually relevant paragraphs matching a query."""
        if self.index is None or not self.chunks:
            return "No vector index built."
        
        query_vector = self.model.encode([query]).astype('float32')
        distances, indices = self.index.search(query_vector, k)
        
        results = []
        for idx in indices[0]:
            if idx < len(self.chunks):
                results.append(self.chunks[idx])
                
        return "\n\n".join(results)
