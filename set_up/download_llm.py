#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from pathlib import Path
import reusables
from box import ConfigBox
from huggingface_hub import hf_hub_download

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('config', type=str)
    args = parser.parse_args()
    config = ConfigBox(reusables.config_dict(args.config))
    hf_hub_download(repo_id=config.model.HUGGINGFACE_REPO_ID, filename=config.model.MODEL_NAME, local_dir=Path(config.model.MODEL_LOCAL_REPO).resolve(), local_dir_use_symlinks=False)