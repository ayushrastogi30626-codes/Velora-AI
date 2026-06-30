import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


class PDFVectorStore:
    def __init__(self):
        self.chunks = []
        self.index = None

    def build_index(self, chunks):
        self.chunks = chunks

        embeddings = model.encode(chunks)

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings))

    def search(self, query, k=3):
        query_vector = model.encode([query])

        distances, indices = self.index.search(np.array(query_vector), k)

        return [self.chunks[i] for i in indices[0]]