from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import List

# RAG custom packages.
from data_chunk_manager import DataChunkManager
from rag import Rag
from vectordb_manager import VectorDbManager


def add_docs(
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

    return ids


app = FastAPI()


# Define a Pydantic model for your request data
class FeedData(BaseModel):
    nid: str
    data: str


class UpdateData(BaseModel):
    nid: str
    ids: List
    data: str


class DeleteData(BaseModel):
    ids: List


class Question(BaseModel):
    question: str


@app.post("/ask")
def ask(data: Question = Body(...)):
    question = data.question

    rag_obj = Rag()
    rag_obj.set_retrieve()
    rag_obj.augment()
    response = rag_obj.generate(question)

    return {"Response": response}


@app.post("/feed/add")
def feed_add(feed_data: FeedData = Body(...)):
    nid = feed_data.nid
    data = feed_data.data

    ids = add_docs(nid=nid, data=data)
    # Return ids
    return {"response": "Document successfully added.", "doc_ids": ids}


@app.post("/feed/update")
def feed_update(feed_data: UpdateData = Body(...)):
    nid = feed_data.nid
    ids = feed_data.ids
    data = feed_data.data

    vectordb_manager = VectorDbManager()

    # Delete with ids passed.
    vectordb_manager.delete_ids(ids=ids)

    # Create fresh documents.
    new_ids = add_docs(nid=nid, data=data)

    # return the ids
    return {"response": "Document successfully updated.", "doc_ids": new_ids}


@app.post("/feed/delete")
def feed_delete(data: DeleteData = Body(...)):
    ids = data.ids

    # Delete with ids passed.
    vectordb_manager = VectorDbManager()
    vectordb_manager.delete_ids(ids=ids)

    return {"response": "Document successfully deleted."}


@app.post('/reset')
def reset():
    vectordb_manager = VectorDbManager()

    return {"Collection_count": vectordb_manager.reset_database()}

@app.get('/all-docs')
def all_docs():
    vectordb_manager = VectorDbManager()

    return {"Collection_count": vectordb_manager.get_all_docs()}
