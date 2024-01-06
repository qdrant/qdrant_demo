
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

## Quick Start <a href="https://replit.com/new/github/qdrant/qdrant_demo"><img align="right" src="https://replit.com/badge/github/qdrant/qdrant_demo" alt="Run on Repl.it"></a>

To launch this demo locally you will need to download data first.

The source of the original data is [https://www.startups-list.com/](https://www.startups-list.com/)

You can download the data via the following command:

```bash
wget https://storage.googleapis.com/generall-shared-data/startups_demo.json -P data/
```

To launch service locally, use

```
docker-compose -f docker-compose-local.yaml up
```

After service is started you can upload initial data to the search engine.

```
# Init neural index
python -m qdrant_demo.init_collection_startups
```

After a successful upload, neural search API will be available at [http://localhost:8000/docs](http://localhost:8000/docs) 

You can play with the data in the following [Colab Notebook](https://colab.research.google.com/drive/1kPktoudAP8Tu8n8l-iVMOQhVmHkWV_L9?usp=sharing).

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1kPktoudAP8Tu8n8l-iVMOQhVmHkWV_L9?usp=sharing)


## Start with Crunchbase data

Alternatively, you can use larger dataset of companies provided by [Crunchbase](https://www.crunchbase.com/).

You will need to register at [https://www.crunchbase.com/](https://www.crunchbase.com/) and get an API key.

```bash
# Download data
wget 'https://api.crunchbase.com/odm/v4/odm.tar.gz?user_key=<CRUNCHBASE-API-KEY>' -O odm.tar.gz
```

Decompress data and put `organizations.csv` into `./data` folder.

```bash
# Decompress data
tar -xvf odm.tar.gz
mv odm/organizations.csv ./data
```

After that, you can run indexing of Crunchbase data into Qdrant.

```bash
# Init neural index
python -m qdrant_demo.init_collection_crunchbase
```
