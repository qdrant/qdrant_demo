
# Semantic Search Engine

You can clone this repo and create your own search engine in a few steps! 
</br> [![Demo](https://img.shields.io/badge/Try%20it%20live%20here!-purple?&style=flat-square&logo=react&logoColor=white)](https://demo.qdrant.tech/) 

You can use this small app to search through a list of popular startups.
<br> - The **neural search** will read the description and look for similar startups.
</br> - The **keyword search** will look up your exact term in the description. 

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

```bash
python -m qdrant_demo.init_collection_startups
```

### 6.  Go to [http://localhost:8000/](http://localhost:8000/) 


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


## What's inside of this app? 

|Software Stack||
|-|-|
|Qdrant|Vector database and a search engine with full-text and semantic capabilities.|
|`all-MiniLM-L6-v2`|The embedding model that turns startup data to vectors.|
|FastEmbed|Qdrant's package that simplifies this vectorization process.|
|Frontend in TypeScript|Basic visuals that you see in the deployed application.|

|Application Components||
|-|-|
|`init_collection_startups.py`|Uploads document embeddings to a Qdrant collection.|
|`neural_searcher.py`|Defines the semantic search process via vector search and optional payload filter.|
|`text_searcher.py`|Defines the keyword search process across startup metadata / payload.|
|`service.py`|Setup instructions for the entire FastAPI application.|
|`config.py`|Defines the directories for code, root, data, and static files|

## init_collection_startups.py
This reads a JSON file containing startup data, restructures the data into a unified schema, and recreates a collection in Qdrant with specified vector and quantization configurations.

In this example, we are turning on Scalar Quantization to make sure less memory is used to process data.

A payload index is created for text search on a specified text field. Finally, it uploads the documents and their metadata to the Qdrant collection. 

## neural_searcher.py
The NeuralSearcher class enables semantic searches. The search method takes a text query and an optional filter, performs a semantic search in the specified collection, and returns the top five results’ metadata. 

## text_searcher.py
The TextSearcher class defines text searches. The search method queries the specified text field for matches and returns the top results, while the highlight method wraps matching query terms in HTML <b> tags for emphasis. 

## service.py
This initializes both searchers. A GET endpoint /api/search allows querying with a text string and a flag to choose between neural and text search methods. 

## config.py
This retrieves environment variables for the Qdrant URL, API key, collection name, and embeddings model. It sets the name of the field used for text data as “document”. 