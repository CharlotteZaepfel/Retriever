"""This file deals w/ building the fitted QA engine and answering questions."""


import sys
from pathlib import Path
from typing import List

from box import ConfigBox
from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import CTransformers
from langchain.schema import Document
from langchain.vectorstores import FAISS

from utils import timekeeper


@timekeeper
def _build_retrieval_qa(
    llm: CTransformers, prompt: str, vectordb: FAISS, config: ConfigBox
) -> RetrievalQA:
    """Builds a RetrievalQA object.

    Args:
        llm: preloaded LLM (from HuggingFace).
        prompt: Few sentences contextualizing the task.
        vectors_path: Path to the dir where the vectorized data is stored.
        config: Dict-like object containing the project params.

    Returns:
        A fitted RestrievalQA object."""
    dbqa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectordb.as_retriever(
            search_kwargs={"k": int(config.retriever.VECTOR_COUNT)}
        ),
        return_source_documents=config.retriever.RETURN_SOURCE_DOCUMENTS,
        chain_type_kwargs={"prompt": prompt},
    )
    return dbqa


@timekeeper
def setup_dbqa(
    llm: CTransformers, vectors_path: Path, config: ConfigBox
) -> RetrievalQA:
    """Instantiates a custom QA object to fit our prompt and data.

    Args:
        llm: preloaded LLM (from HuggingFace).
        vectors_path: Path to the dir where the vectorized data is stored.
        config: Dict-like object containing the project params.

    Returns:
        This is a description of what is returned."""
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
    )
    vectordb = FAISS.load_local(vectors_path, embeddings)
    qa_prompt = PromptTemplate(
        template=config.task.QA_TEMPLATE,
        input_variables=["context", "question"]
    )
    dbqa = _build_retrieval_qa(llm, qa_prompt, vectordb, config)
    return dbqa


def display_sources(source_docs: List[Document], docs_format: str) -> None:
    """Displays where the answer can be found in data.

    Args:
        source_docs: List of processed documents.
        docs_format: Files format [*.pdf|*.html]."""
    sys.stdout.write("SOURCES :")
    for i, doc in enumerate(source_docs):
        if docs_format == "*.pdf":
            sys.stdout.write(
                f'\n=> {doc.metadata["source"]}(p.{doc.metadata["page"]}):\n'
            )
        else:
            sys.stdout.write(f'\n=> {doc.metadata["source"]}\n')
        sys.stdout.write(doc.page_content)
        sys.stdout.write("\n")
