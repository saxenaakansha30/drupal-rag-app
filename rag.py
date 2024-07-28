# Provides RAG implementation.
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

from llm_integration import LlmIntegration
from retriever import Retriever

class Rag:

    retriever = None
    chain = None

    def __init__(self):
        self.retriever = Retriever()
        self.llm_obj = LlmIntegration()
        self.llm_obj.set_modal(model_name="mistral")

    # Retrieve the context from the vector database.
    def set_retrieve(self):
        self.retriever = self.retriever.get_retriever()

    # Augment the context with original prompt.
    def augment(self):
        self.chain = ({"context": self.retriever, "question": RunnablePassthrough()}
                      | self.llm_obj.get_prompt()
                      | self.llm_obj.get_modal()
                      | StrOutputParser())

    # Generate response from the LLM.
    def generate(self, question: str):
        if not self.chain:
            return "Augmentation is not done yet."

        return self.chain.invoke(question)

    # Reset the flow.
    def reset(self):
        self.chain = None
        self.retriever = None