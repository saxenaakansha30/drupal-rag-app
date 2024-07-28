from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.utils import filter_complex_metadata


class DataChunkManager:

    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=20)

    def generate_chunk(self, document):
        chunks = self.text_splitter.split_documents(document)
        chunks = filter_complex_metadata(chunks)

        return chunks

    def create_document(self, text):
        document = self.text_splitter.create_documents(text)

        return document
