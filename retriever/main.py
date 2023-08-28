#!/usr/bin/env python

"""This module extracts information from documents using llama2."""


import argparse
import os
import sys
from pathlib import Path

import reusables
from box import ConfigBox
from langchain.llms import CTransformers

from compute_answer import display_sources, setup_dbqa
from logger import set_logger
from process_db import create_and_store_embeddings
from utils import timekeeper


log = set_logger(__name__)


@timekeeper
def main(config: ConfigBox):
    """Extracts information from documents using llama2.

    Args:
        config: Dict-like object containing the project params."""
    model_path = Path(
        config.project.LOCAL_PATH,
        config.model.MODEL_LOCAL_REPO,
        config.model.MODEL_NAME,
    )
    if not model_path.is_file():
        log.critical(f"The model {model_path} cannot be found.")
        sys.exit()
    vectors_path = Path(
        config.project.LOCAL_PATH,
        config.data_parsing.DB_FAISS_PATH
    )
    if not os.access(vectors_path, os.W_OK):
        log.critical(f"The folder {vectors_path} is not writable.")
        sys.exit()
    # Step 1: Load and process data
    create_and_store_embeddings(vectors_path, config)
    # Step 2: Load model
    llm = CTransformers(
        model=str(model_path),
        model_type=config.model.MODEL_TYPE,
        config={
            "max_new_tokens": int(config.model.MAX_NEW_TOKENS),
            "temperature": float(config.model.TEMPERATURE),
        },
    )
    # Step 3: Set up a custom QA engine
    dbqa = setup_dbqa(llm, vectors_path, config)
    for i, question in config.QUESTIONS.items():
        log.info(f"Starting {i}...")
        # Step 4: Parse question into the QA engine
        response = dbqa({"query": question})
        # Step 5: Display QA response and justifications
        sys.stdout.write(f'\nQUESTION: \n{question}\n\n')
        sys.stdout.write(f'\nANSWER: \n{response["result"]}\n\n')
        source_docs = response["source_documents"]
        display_sources(source_docs, config.data.FILES_FORMAT)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=str)
    args = parser.parse_args()
    # Parse and check config
    try:
        config = ConfigBox(reusables.config_dict(args.config))
    except FileNotFoundError:
        log.critical(f"The path {args.config} to config cannot be found.")
        sys.exit()
    main(config)
