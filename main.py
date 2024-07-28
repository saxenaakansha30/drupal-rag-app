from fastapi import FastAPI

# RAG custom packages.
from vectordb_manager import VectorDbManager
from rag import Rag
from data_chunk_manager import DataChunkManager

from typing import List

app = FastAPI()


@app.get("/ask")
def ask(
        question: str
):

    rag_obj = Rag()
    rag_obj.set_retrieve()
    rag_obj.augment()
    response = rag_obj.generate(question)

    return {"Response": response}


@app.post("/feed/add")
def feed_add(
        nid: str,
        data: str,
):
    chunk_manager = DataChunkManager()
    document = chunk_manager.create_document([data])
    chunks = chunk_manager.generate_chunk(document=document)

    ids = []
    for count in range(1, len(chunks) + 1):
        ids.append('nid_' + nid + '_' + str(count))

    vector_manager = VectorDbManager()
    vector_manager.store_data(chunks, ids=ids)

    # Return ids
    return {"response": "Document successfully added.", "doc_ids": ids}


@app.get("/feed/update")
def feed_update(
        nid: str,
        ids: List,
        data: str,
):

    vectordb_manager = VectorDbManager()

    # Delete with ids passed.
    vectordb_manager.delete_ids(ids=ids)

    # Add as fresh entry.
    chunk_manager = DataChunkManager()
    document = chunk_manager.create_document(data)
    chunks = chunk_manager.generate_chunk(document=document)

    new_ids = []
    for count in range(1, len(chunks) + 1):
        new_ids.append('nid_' + nid + '_' + str(count))

    vectordb_manager.store_data(chunks, ids=new_ids)

    # return the ids
    return {"response": "Document successfully updated.", "doc_ids": new_ids}


@app.get("/feed/delete")
def feed_delete(
        nid: int,
        ids: List,
):
    # Delete with ids passed.
    vectordb_manager = VectorDbManager()
    vectordb_manager.delete_ids(ids=ids)

    return {"response": "Document successfully deleted."}

@app.get('/test')
def test():
    vectordb_manager = VectorDbManager()
    return {"Collection_count": vectordb_manager.get_all_docs()}

@app.get('/reset')
def test():
    vectordb_manager = VectorDbManager()
    return {"Collection_count": vectordb_manager.reset_database()}