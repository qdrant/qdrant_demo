import json
import os.path
import logging
from datetime import datetime

from qdrant_client import QdrantClient, models
from tqdm import tqdm

from qdrant_demo.config import DATA_DIR, QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME, TEXT_FIELD_NAME, EMBEDDINGS_MODEL


def upload_embeddings():
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]} - INFO - Initializing Qdrant client...")
    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        prefer_grpc=True,
    )

    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]} - INFO - Setting embedding model: {EMBEDDINGS_MODEL}")
    client.set_model(EMBEDDINGS_MODEL)

    payload_path = os.path.join(DATA_DIR, 'startups_demo.json')
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]} - INFO - Loading data from file: {payload_path}")
    payload = []
    documents = []

    with open(payload_path) as fd:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]} - INFO - Processing data...")
        for line in fd:
            obj = json.loads(line)
            documents.append(obj.pop('description'))
            obj["logo_url"] = obj.pop("images")
            obj["homepage_url"] = obj.pop("link")
            payload.append(obj)
    
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]} - INFO - Data processed: {len(documents)} documents")

    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]} - INFO - Recreating collection: {COLLECTION_NAME}")
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=client.get_fastembed_vector_params(on_disk=True),
        quantization_config=models.ScalarQuantization(
            scalar=models.ScalarQuantizationConfig(
                type=models.ScalarType.INT8,
                quantile=0.99,
                always_ram=True
            )
        ),
        optimizers_config=models.OptimizersConfigDiff(
            max_optimization_threads=2
        )
    )

    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]} - INFO - Creating payload index for field: {TEXT_FIELD_NAME}")
    client.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name=TEXT_FIELD_NAME,
        field_schema=models.TextIndexParams(
            type=models.TextIndexType.TEXT,
            tokenizer=models.TokenizerType.WORD,
            min_token_len=2,
            max_token_len=20,
            lowercase=True,
        )
    )

    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]} - INFO - Uploading documents to collection...")
    client.add(
        collection_name=COLLECTION_NAME,
        documents=documents,
        metadata=payload,
        ids=tqdm(range(len(payload))),
        parallel=0,
    )
    
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]} - INFO - Upload completed successfully!")


if __name__ == '__main__':
    upload_embeddings()
