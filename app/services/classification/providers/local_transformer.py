import numpy as np
from typing import Any
from sentence_transformers import SentenceTransformer

from app.services.classification.providers.base import BaseClassificationProvider

class LocalTransformerProvider(BaseClassificationProvider):
    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        self.model = SentenceTransformer(model_name)
        
    def get_embeddings(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(texts)
        if isinstance(embeddings, np.ndarray):
            return embeddings.tolist()  # type: ignore
        return [list(map(float, e)) for e in embeddings]

    def get_semantic_classification(self, text: str, categories: list[str]) -> tuple[str, float]:
        if not categories:
            return "", 0.0
            
        text_emb = np.array(self.get_embeddings([text]))
        cat_embs = np.array(self.get_embeddings(categories))
        
        # Compute cosine similarity manually using numpy
        dot = np.dot(text_emb, cat_embs.T)[0]
        norm_t = np.linalg.norm(text_emb, axis=1)[0]
        norm_c = np.linalg.norm(cat_embs, axis=1)
        similarities = dot / (norm_t * norm_c)
        
        best_idx = int(np.argmax(similarities))
        best_score = float(similarities[best_idx])
        
        return categories[best_idx], best_score
