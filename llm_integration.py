from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama

class LlmIntegration:

    def __init__(self):
        self.prompt = PromptTemplate.from_template(
            """
            <s> [INST] You are an assistant for question-answering tasks. Use the following pieces of retrieved context
            to answer the question. If you don't know the answer, just say that you don't know. Use three sentences
              maximum and keep the answer concise. [/INST] </s>
            [INST] Question: {question}
            Context: {context}
            Answer: [/INST]
            """
        )

    def set_modal(self, model_name: str):
        self.model = ChatOllama(model=model_name)

    def get_modal(self):
        return self.model

    def get_prompt(self):
        return self.prompt