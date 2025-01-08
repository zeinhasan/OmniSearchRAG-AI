# models/faiss_handler.py
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class FaissHandler:
    def __init__(self):
        # Load a pre-trained sentence transformer model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.dimension = 384  # Dimension of the embeddings
        self.index = faiss.IndexFlatL2(self.dimension)  # FAISS index

    def add_documents(self, documents: list):
        """
        Add documents to the FAISS index.
        """
        embeddings = self.model.encode(documents)
        self.index.add(np.array(embeddings))

    def search(self, query: str, k: int = 3) -> list:
        """
        Search for the most relevant documents.
        """
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_embedding), k)
        return indices[0].tolist()