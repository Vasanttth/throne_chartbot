"""
ingest.py
Build vector database from TXT dataset only.
Run: python ingest.py
"""

import os
import shutil

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

DATA_PATH = "data"
VECTORSTORE_PATH = "vectorstore"
COLLECTION_NAME = "throne_recliners"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def clear_vectorstore():
    if os.path.exists(VECTORSTORE_PATH):
        print("Deleting old vectorstore...")
        shutil.rmtree(VECTORSTORE_PATH)


def load_documents():
    loader = DirectoryLoader(
        DATA_PATH,
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True,
    )

    documents = loader.load()
    print(f"Loaded {len(documents)} TXT document(s)")
    return documents


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=150,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks")
    return chunks


def build_vectorstore(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBED_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTORSTORE_PATH,
        collection_name=COLLECTION_NAME,
    )

    print("Vector database created successfully.")


if __name__ == "__main__":
    print("Building Throne Recliners knowledge base...")

    clear_vectorstore()

    documents = load_documents()

    if not documents:
        raise ValueError("No .txt files found inside the data folder.")

    chunks = split_documents(documents)

    build_vectorstore(chunks)

    print("Knowledge base built successfully.")