from langchain_community.vectorstores import chroma
from langchain_community.embeddings import fastembed

from typing import List

class VectorDbManager:

    def __init__(self):
        self.vectordb = chroma.Chroma(persist_directory="chroma_data",
                                      embedding_function=fastembed.FastEmbedEmbeddings())
    def store_data(self, chunks, ids: list):
        print(ids);
        print(chunks);

        vectordb = chroma.Chroma.from_documents(
            documents=chunks,
            embedding=fastembed.FastEmbedEmbeddings(),
            persist_directory="chroma_data",
            ids=ids
        )
        vectordb.persist()

    def get_vector_store(self):
        return self.vectordb

    def delete_data(self, doc_id: str):
        self.vectordb._collection.delete(ids=[doc_id])

    def delete_ids(self, ids: List):
        self.vectordb._collection.delete(ids=ids)

    def get_doc_count(self):
        return self.vectordb._collection.count()

    def get_all_docs(self):
        return self.vectordb.get()

    def reset_database(self):
        collections = self.get_all_docs()
        self.vectordb._collection.delete(ids=collections['ids'])

    def get_doc(self, id: str):
        return self.vectordb.get(id)