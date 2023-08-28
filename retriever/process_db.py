"""This file deals with data procesing and embedding storage."""

from pathlib import Path

from box import ConfigBox
from langchain.document_loaders import (DirectoryLoader, PyPDFLoader,
                                        UnstructuredHTMLLoader)
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS

from utils import timekeeper


@timekeeper
def create_and_store_embeddings(vectors_path: Path, config: ConfigBox) -> None:
    """Load PDF files from data path,
    Chunk, vectorize the text,
    Build and persist FAISS vector store.

    Args:
        vectors_path: Path to the dir where the vectorized data is stored.
        config: Dict-like object containing the project params."""
    loaders = {
        "PyPDFLoader": PyPDFLoader,
        "UnstructuredHTMLLoader": UnstructuredHTMLLoader,
    }
    loader = DirectoryLoader(
        config.data.CORPUS_PATH,
        glob=config.data.FILES_FORMAT,
        loader_cls=loaders[config.data.CORPUS_LOADER],
        show_progress=True,
    )
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=int(config.data_parsing.CHUNK_SIZE),
        chunk_overlap=int(config.data_parsing.CHUNK_OVERLAP),
    )
    texts = text_splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
    )
    vectorstore = FAISS.from_documents(texts, embeddings)
    vectorstore.save_local(vectors_path)
