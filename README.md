
# Startup Hybrid Search Engine

You can clone this repo and create your own search engine in a few steps!
</br> [![Demo](https://img.shields.io/badge/Try%20it%20live%20here!-purple?&style=flat-square&logo=react&logoColor=white)](https://demo.qdrant.tech/)

Search through a list of startups by their descriptions, and switch between three modes to see how each one ranks:

- **Semantic** embeds the query with a dense model and ranks by vector similarity.
- **Keyword** matches the exact terms in the description through a full-text index.
- **Hybrid** runs both and fuses the results with Reciprocal Rank Fusion (RRF). This is the default.

![Startup Search Demo](demo.gif)

## Prerequisites
- Python (v.3.11)
- Docker

## Setup

### 1. Setup the virtual environment

```python
python -m venv .venv
source .venv/bin/activate
```

### 2. Install required dependencies

```bash
pip install poetry
poetry install
```

### 3. Download the dataset

```bash
wget https://storage.googleapis.com/generall-shared-data/startups_demo.json -P data/
```

### 4. Deploy the service

```bash
docker-compose -f docker-compose-local.yaml up
```

### 5. Upload data to the application

Running against a local Qdrant container, set `CLOUD_INFERENCE=0` so the client
embeds the documents locally with fastembed:

```bash
CLOUD_INFERENCE=0 python -m qdrant_demo.init_collection_startups
```

Against Qdrant Cloud, leave `CLOUD_INFERENCE=1` (the default) and the same
`models.Document` calls embed server-side, so nothing is downloaded locally.

### 6.  Go to [http://localhost:8000/](http://localhost:8000/)


## Search modes

The API is `GET /api/search?q=<query>&mode=<semantic|keyword|hybrid>`. Hybrid is
the default when no mode is given.

- **semantic**: dense search on the `dense` vector (mxbai-embed-large-v1).
- **keyword**: full-text match on the `document` field.
- **hybrid**: prefetches the dense and `sparse` (bm25) vectors and fuses them with RRF.

The older `neural` flag still works for backward compatibility: `neural=true` is
semantic, `neural=false` is keyword.

## Using a larger dataset with more startups

You can add a larger dataset of companies provided by [Crunchbase](https://www.crunchbase.com/).

For this, you will need to register at [https://www.crunchbase.com/](https://www.crunchbase.com/) and get an API key.

### 1. Download the data

```bash
wget 'https://api.crunchbase.com/odm/v4/odm.tar.gz?user_key=<CRUNCHBASE-API-KEY>' -O odm.tar.gz
```

### 2. Decompress the data and add `organizations.csv` to `./data` folder.

```bash
tar -xvf odm.tar.gz
mv odm/organizations.csv ./data
```

### 3. Now you can index new Crunchbase data into Qdrant

```bash
python -m qdrant_demo.init_collection_crunchbase
```

> The hosted demo runs a larger startups collection (roughly 3M profiles) built
> the same way. This repo's scripts build the smaller `startups_demo.json` set by
> default; point `COLLECTION_NAME` at your own collection to serve a different one.


## What's inside of this app?

|Software Stack||
|-|-|
|Qdrant|Vector search engine with dense, sparse, and full-text retrieval.|
|`mxbai-embed-large-v1`|The 1024-dimensional dense embedding model.|
|`Qdrant/bm25`|The sparse keyword model; IDF is applied at query time by the collection.|
|Qdrant Cloud Inference|Embeds queries and documents server-side, with a local fastembed fallback.|
|Frontend in TypeScript|Basic visuals that you see in the deployed application.|

|Application Components||
|-|-|
|`init_collection_startups.py`|Builds the collection with named `dense` and `sparse` vectors and uploads the startups.|
|`neural_searcher.py`|Runs semantic and hybrid (dense + bm25, RRF) search.|
|`text_searcher.py`|Runs keyword search across the startup metadata / payload.|
|`service.py`|Setup instructions for the entire FastAPI application.|
|`config.py`|Defines the directories for code, root, data, and static files.|

## init_collection_startups.py
Reads the startups JSON, renames the payload to the schema the frontend reads
(`document`, `logo_url`, `homepage_url`), and creates a collection with a named
`dense` vector, a `sparse` bm25 vector with `modifier=IDF`, and a text index on
`document`. Scalar quantization is enabled to reduce memory. Both vectors are
embedded through `models.Document`, so the same script works against Qdrant Cloud
(server-side) or a local container (client-side fastembed).

## neural_searcher.py
The NeuralSearcher class runs semantic and hybrid search. It embeds the query with
mxbai, and for hybrid it prefetches the dense and bm25 vectors and fuses them with
RRF. It returns the result payloads plus a small stats object (mode, model, and
score type).

## text_searcher.py
The TextSearcher class runs keyword search. It filters the `document` text index
for matches, ranks them by term frequency, and wraps matching terms in HTML `<b>`
tags for emphasis.

## service.py
This initializes both searchers and exposes `GET /api/search`, which takes a query
and a `mode` (semantic, keyword, or hybrid). An unknown mode returns a 400.

## config.py
This retrieves environment variables for the Qdrant URL, API key, collection name,
and the dense and sparse embedding models. It sets the payload text field to
`document`.
