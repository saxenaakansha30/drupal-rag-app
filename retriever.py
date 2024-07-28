# Provides the vector database as retriever
from vectordb_manager import VectorDbManager
class Retriever:

    def __init__(self):
        vector_manager = VectorDbManager()
        self.vector_store = vector_manager.get_vector_store()
        self.retriever = None

    def get_retriever(self):
        if not self.retriever:
            self.retriever = self.vector_store.as_retriever(
                search_type="similarity_score_threshold",
                search_kwargs={
                    "k": 3,
                    "score_threshold": 0.5,
                },
            )

        return self.retriever

