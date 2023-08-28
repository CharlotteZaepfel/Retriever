.ONESHELL:
.PHONY: help prepare-dev test lint run doc venv env-test
PROJECT_ENV=llm_env
PROJECT_NAME=information_retriever
PROJECT_MAIN_MODULE=retriever
PROJECT_VERSION=$(shell cat VERSION)
PYTHON_VERSION=3.10.12


PYTHON=python3


install:
	conda create --name ${PROJECT_ENV} python=${PYTHON_VERSION} pip

dep: ## install required dependencies for build.
	conda run -n ${PROJECT_ENV} $(PYTHON) -m pip install flake8 black isort mypy
	conda run -n ${PROJECT_ENV} $(PYTHON) -m pip install pytest
	conda run -n ${PROJECT_ENV} $(PYTHON) -m pip install pre-commit

env-dev: dep## init dev environnement.
	conda install -n ${PROJECT_ENV} -c conda-forge langchain sentence-transformers
	conda install -n ${PROJECT_ENV} -c pytorch pytorch torchvision torchaudio cpuonly
	conda install -n ${PROJECT_ENV} -c pytorch faiss-cpu=1.7.4 mkl=2021 blas=1.0=mkl
	conda run -n ${PROJECT_ENV} $(PYTHON) -m pip install -r requirements.txt
	conda run -n ${PROJECT_ENV} $(PYTHON) set_up/download_llm.py set_up/install_config.ini

download:
	conda run -n ${PROJECT_ENV} $(PYTHON) set_up/download_llm.py $(CONFIG)

env-prod: dep## init prod environnement.
	$(PYTHON) -m pip install -r requirements.txt

welcome: dep env-dev ## Init everything to get started

lint: ## Check error with code
	@echo "Flake8:" && $(PYTHON) -m flake8 $(PROJECT_MAIN_MODULE) && \
	echo "Mypy:" && $(PYTHON) -m mypy setup.py $(PROJECT_MAIN_MODULE) --namespace-packages

fmt: ## Format code.
	@$(PYTHON) -m black $(PROJECT_MAIN_MODULE)
	@$(PYTHON) -m isort $(PROJECT_MAIN_MODULE)

test: venv ## run test.
	@$(PYTHON) -m pytest -v tests/

run:
	conda run --no-capture-output -n ${PROJECT_ENV} $(PYTHON) -u retriever/main.py $(CONFIG)

clean:
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm *.rdb
	rm .env
	rm .coverage

help: ## Display this help screen
	@grep -h -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'