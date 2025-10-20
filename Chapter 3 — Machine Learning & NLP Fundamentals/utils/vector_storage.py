from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class VectorMemory:
    """Simple in-memory vector store for agent embeddings."""
    def __init__(self):
        self.embeddings = []
        self.texts = []

    def add(self, text, embedding):
        self.embeddings.append(embedding)
        self.texts.append(text)

    def retrieve(self, query_vector, top_k=1):
        """Retrieve most similar memories using cosine similarity."""
        if not self.embeddings:
            return []
        similarities = cosine_similarity([query_vector], self.embeddings)[0]
        top_indices = np.argsort(similarities)[::-1][:top_k]
        return [(self.texts[i], similarities[i]) for i in top_indices]
