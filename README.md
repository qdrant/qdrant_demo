# Startup Hybrid Search

[![Try it live](https://img.shields.io/badge/Try%20it%20live%20here!-purple?&style=flat-square&logo=react&logoColor=white)](https://demo.qdrant.tech/)

Clone this repo and stand up your own search engine in a few steps. It searches a
catalog of startups by their descriptions and lets you switch between three
retrieval modes, so you can feel the difference between them on the same data.

## How It Works

One query, three ways to rank it:

- **Semantic** embeds the query with a dense model (mxbai-embed-large-v1) and ranks by vector similarity. Good for meaning, weak on exact terms.
- **Keyword** matches the exact words through a full-text index. Good for names and specific terms, blind to meaning.
- **Hybrid** runs both and fuses them with Reciprocal Rank Fusion. It is the default, and usually the best of the two.

Qdrant does the retrieval end to end: a named `dense` vector for semantic, a
`sparse` bm25 vector for keyword, and RRF to combine them.

## Quickstart

Runs fully locally against a Qdrant container. No cloud account needed.

**Prerequisites:** Python 3.11 and Docker.

**1. Create the virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate
```

**2. Install dependencies**

```bash
pip install poetry
poetry install
```

**3. Download the dataset**

```bash
wget https://storage.googleapis.com/generall-shared-data/startups_demo.json -P data/
```

**4. Start Qdrant and the app**

```bash
docker-compose -f docker-compose-local.yaml up
```

**5. Load the data**

Locally, set `CLOUD_INFERENCE=0` so the client embeds with fastembed:

```bash
CLOUD_INFERENCE=0 python -m qdrant_demo.init_collection_startups
```

**6. Open the app**

Go to [http://localhost:8000/](http://localhost:8000/) and start searching.

## Run Against Qdrant Cloud

Point the app at a Qdrant Cloud cluster and let it embed server-side, so nothing
downloads locally. Set these before loading data and starting the app:

```bash
export QDRANT_URL="https://<your-cluster>.cloud.qdrant.io:6333"
export QDRANT_API_KEY="<your-api-key>"
export CLOUD_INFERENCE=1   # the default
```

The same `python -m qdrant_demo.init_collection_startups` builds the collection,
this time with Qdrant Cloud Inference doing the embedding.

## The Search API

```
GET /api/search?q=<query>&mode=<semantic|keyword|hybrid>
```

`mode` defaults to `hybrid`. The older `neural` flag still works: `neural=true`
maps to semantic, `neural=false` to keyword. An unknown mode returns a 400.

## Scale Up With Crunchbase Data

Swap in a larger company dataset from [Crunchbase](https://www.crunchbase.com/).
Register for an API key, then:

```bash
# 1. Download and unpack
wget 'https://api.crunchbase.com/odm/v4/odm.tar.gz?user_key=<CRUNCHBASE-API-KEY>' -O odm.tar.gz
tar -xvf odm.tar.gz
mv odm/organizations.csv ./data

# 2. Build the collection (same schema as the startups one)
python -m qdrant_demo.init_collection_crunchbase
```

> The hosted demo runs a larger startups collection (roughly 3M profiles) built
> the same way. This repo builds the smaller `startups_demo.json` set by default.
> Point `COLLECTION_NAME` at your own collection to serve a different one.

## How It's Built

| Piece | Role |
|-|-|
| Qdrant | Vector search engine handling dense, sparse, and full-text retrieval. |
| `mxbai-embed-large-v1` | The 1024-dimensional dense embedding model. |
| `Qdrant/bm25` | The sparse keyword model. The collection applies IDF at query time. |
| Qdrant Cloud Inference | Embeds queries and documents server-side, with a local fastembed fallback. |
| React + TypeScript frontend | The UI you see in the deployed app. |

Search flow: the query is embedded by the same models the documents were, then
dense and sparse results come back from Qdrant and, in hybrid mode, get fused with
RRF before the payloads are returned to the UI.

## Project Structure

| File | Responsibility |
|-|-|
| `init_collection_startups.py` | Builds the collection with named `dense` and `sparse` vectors, a text index, and the renamed payload, then uploads the startups. |
| `init_collection_crunchbase.py` | The same build for the larger Crunchbase dataset. |
| `neural_searcher.py` | Semantic and hybrid (dense + bm25, RRF) search. |
| `text_searcher.py` | Keyword search over the full-text index, with match highlighting. |
| `service.py` | The FastAPI app and the `/api/search` endpoint. |
| `config.py` | Environment configuration: Qdrant connection, collection, models, and vector names. |
