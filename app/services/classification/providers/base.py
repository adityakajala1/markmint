import abc

class BaseClassificationProvider(abc.ABC):
    
    @abc.abstractmethod
    def get_embeddings(self, texts: list[str]) -> list[list[float]]:
        pass
        
    @abc.abstractmethod
    def get_semantic_classification(self, text: str, categories: list[str]) -> tuple[str, float]:
        pass
