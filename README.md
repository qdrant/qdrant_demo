
# Neural search demo 
## With Qdrant + BERT + FastAPI

This repository contains a code for Neural Search for startups [demo](https://demo.qdrant.tech).

The demo is based on the vector search engine [Qdrant](https://github.com/qdrant/qdrant).

## Requirements
Install python requirements:

```
pip install poetry
poetry install
```

You will also need [Docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/)

## Quick Start

To launch this demo locally you will need to prepare data first.

The source of the original data is [https://www.startups-list.com/](https://www.startups-list.com/)

Code for initial data preparation could be found in [Colab Notebook](https://colab.research.google.com/drive/1kPktoudAP8Tu8n8l-iVMOQhVmHkWV_L9?usp=sharing).

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1kPktoudAP8Tu8n8l-iVMOQhVmHkWV_L9?usp=sharing)

After evaluating Colab you should get startup records in file `./data/startups.json` and encoded vectors in file `./data/startup_vectors.npy`

To launch service locally, use

```
docker-compose -f docker-compose-local.yaml up
```

After service is started you can upload initial data to the search engine.


```
# Init neural index
python -m qdrant_demo.init_vector_search_index
# Init full-text index
python -m qdrant_demo.init_text_search_index
```

After a successful upload, neural search API will be available at [http://localhost:8000/docs](http://localhost:8000/docs) 
