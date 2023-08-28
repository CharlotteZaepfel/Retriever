# Retriever

This project is a QA-based information retriever using llama2.<br>

Retriever allows us to run llama2 on a CPU-only machine.<br>
It was written as a toy project to discover the model using minimal ressources and can be used both : 
- to experiment as is with different data 
- to build from its structure a more performance-driven version.<br>

If you are using Retriever as is on your machine, please keep in mind that the model can take up to some minutes to answer a question and also that we are using the smallest llama2 model.


## Tools and dependancies

### Embeddings
- [C Transformers](https://github.com/marella/ctransformers): Python bindings for the Transformer models implemented in C/C++ using GGML library
- [FAISS](https://faiss.ai/index.html): Open-source library implemented in C++ for efficient similarity search and clustering of dense vectors.
- [Sentence-Transformers](https://www.sbert.net/docs/pretrained_models.html): Open-source pre-trained transformer models for embedding text.The model [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) maps sentences and paragraphs to a 384 dimensional dense vector space and can be used for tasks like clustering or semantic search.

These tools are managed by [LangChain](https://www.langchain.com/), a powerful framework agregating various tools to develop LM-powered applications.

### LLM

- Llama-2-7B-Chat: Open-source fine-tuned Llama 2 model designed for chat dialogue. Leverages publicly available instruction datasets and over 1 million human annotations.

## Requirements

This project will need certain dependencies for you dev environnements :
- [conda](https://conda.io/projects/conda/en/latest/index.html)<br>
- a [HuggingFace](https://huggingface.co/) account

You also need to have Python 3.10 installed on your computer as FAISS is not compatible on date (update 08/15/2023) !<br>

Finally, the use of llama2 is governed by the Meta license so you will need to fill this [form](https://ai.meta.com/resources/models-and-libraries/llama-downloads/) before requesting access.

## Install

You will need first to [install conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) if it's not done.<br>
The first step before starting to dev is to unsure that the minimum dependencies are installed before you start working:

Create a conda virtual environement:

```
make install
```

Install dependencies:
```
make welcome
```

And that's it, you ready to go !


## Run 

There is a default `main.py` with this project, you can run it by using:

```bash
$ make run CONFIG=config.ini
```

You can duplicate and modify the config file to fit your experiments.

## Documentation

### Config.ini
| Parameter                 | Type        | Description                                                      | 
| :------------------------ | :---------- | :--------------------------------------------------------------- |
| `LOCAL_PATH`              | `str`       | The absolute path to the repository.                             |
| `CORPUS_PATH`             | `str`       | The sub-path to the data.                                        |
| `FILES_FORMAT`            | `str`       | The format of the files [\*.pdf\|\*.html].                       | 
| `CORPUS_LOADER`           | `str`       | The loader correponding to the files format.                     |
| `CHUNK_SIZE`              | `int`       | The number of characters in each split of files.                 |
| `CHUNK_OVERLAP`           | `int`       | The number of characters overlaping previous split.              |
| `DB_FAISS_PATH`           | `str`       | The sub-path to your processed embeddings.                       |
| `VECTOR_COUNT`            | `int`       | A number of relevant documents to retrieve.                      |
| `RETURN_SOURCE_DOCUMENTS` | `bool`      | Whether to display the source documents.                         |
| `MODEL_TYPE`              | `str`       | The family of LLM to use (default: llama).                       |
| `HUGGINGFACE_REPO_ID`     | `str`       | The batch size to use for evaluating tokens in a single prompt.  |
| `MODEL_NAME`              | `str`       | The number of threads to use for evaluating tokens.              |
| `MAX_NEW_TOKENS`          | `int`       | The maximum context length to use.                               |
| `TEMPERATURE`             | `float`     | The val used to module the next token probabilities in LLM [0-1].|
| `QA_TEMPLATE`             | `str`       | The prompt setting the context for the QA.                       |
| `QUESTIONS`               | `List[str]` | The list of questions for the model.                             |

## Manage

### Add other models from huggingface

Inside the conda virtual environement:

```bash
make download CONFIG=[set_up/install_config.ini]
```

### Run Test

```bash
$ make test
```

### Run Linter

```bash
$ make lint
```

### Format code

```bash
$ make fmt
```

### Clean all project file

```bash
$ make clean
```

## Example of output

This is an example of output with original config.ini of the Harry_Potter.pdf :


> QUESTION: 
> What is the sport that wizards play with broomsicks?
> 
> 
> ANSWER: 
> 
> 
> Answer: Ah, a fellow seeker of knowledge! adjusts glasses Quidditch, you say? Well, my dear friend, let me tell you all about this most intriguing and exhilarating sport played by the wizarding community! 🧙‍♂️
> 
> Quidditch, as it turns out, is a game of skill, strategy, and bravery. Imagine a combination of football, basketball, and flying on broomsticks! 🚀 It's a sport that has been enjoyed by wizards for centuries, with its origins dating back to the early days of Hogwarts School of Witchcraft and Wizardry. 🏰
> 
> The game is played on a large, rectangular field, typically located in an open area such as a park or a stadium. The objective of Quidditch is simple: score points by throwing the quaffle (a ball) through one of six hoops, each placed atop a tall pillar called a goalpost. 🏆
> 
> SOURCES :
> => data/Harry_Potter.pdf(p.64):
> ‘So what is Quidditch?’ 
> ‘It’s our sport. Wizard sport. It’s like – like football in the 
> Muggle world – everyone follows Quidditch – played up in the air on broomsticks and there’s four balls – sorta hard ter explain the rules.’
> 
> => data/Harry_Potter.pdf(p.127):
> score,’ Harry recited. ‘So – that’s sort of like basketball on broom-sticks with six hoops, isn’t it?’ 
> ‘What’s basketball?’ said Wood curiously . 
> ‘Never mind,’ said Harry quickly . 
> ‘Now , there’s another player on each side who’s called the
