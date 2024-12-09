# FastAPI RAG Server

This FastAPI application provides an API for the RAG (Retrieve, Augment, Generate) system, allowing users to ask questions and receive generated responses.

## Required Packages

`pip install fastapi uvicorn langchain langchain-community fastembed chromadb`

## Getting Started

To get the server running locally:

1. Clone the repository
2. Install the requirements:
3. Run the development server:
    `uvicorn main:app --port 8086  --reload`

## API Endpoints

- `POST /ask`: Submit a question and receive a response from LLM.
- `POST /feed/add`: Stores data to chroma vector store.
- `POST /feed/update`: Update data stored in chroma vector store.
- `POST /feed/delete`: Delete data stored in chroma vector store.
- `POST /reset`: Reset the chroma vector storage.
- `POST /all-docs`: Lists all documents stored in vector storage.
