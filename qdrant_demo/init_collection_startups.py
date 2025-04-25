import json
import os.path
from typing import Iterable

from qdrant_client import QdrantClient, models
from tqdm import tqdm

from qdrant_demo.config import DATA_DIR, QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME, TEXT_FIELD_NAME, EMBEDDINGS_MODEL


def read_points() -> Iterable[models.PointStruct]:
    payload_path = os.path.join(DATA_DIR, 'startups_demo.json')
    with open(payload_path) as fd:
        for idx, line in enumerate(fd):
            obj = json.loads(line)

            # Rename fields to unified schema
            obj["logo_url"] = obj.pop("images")
            obj["homepage_url"] = obj.pop("link")
            obj["document"] = obj.pop("description")
            yield models.PointStruct(
                id=idx,
                vector=models.Document(
                    text=obj["document"],
                    model=EMBEDDINGS_MODEL,
                ),
                payload=obj,
            )


def upload_embeddings():
    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        prefer_grpc=True,
    )

    client.set_model(EMBEDDINGS_MODEL)

    payload_path = os.path.join(DATA_DIR, 'startups_demo.json')
    payload = []
    documents = []

    with open(payload_path) as fd:
        for line in fd:
            obj = json.loads(line)
            # Rename fields to unified schema
            documents.append(obj.pop('description'))
            obj["logo_url"] = obj.pop("images")
            obj["homepage_url"] = obj.pop("link")
            payload.append(obj)

    if client.collection_exists(COLLECTION_NAME):
        print(f"Collection {COLLECTION_NAME} already exists. Remove it first.")
        client.delete_collection(COLLECTION_NAME)

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=client.get_embedding_size(EMBEDDINGS_MODEL),
            distance=models.Distance.COSINE,
            on_disk=True,
        ),
        # Quantization is optional, but it can significantly reduce the memory usage
        quantization_config=models.ScalarQuantization(
            scalar=models.ScalarQuantizationConfig(
                type=models.ScalarType.INT8,
                quantile=0.99,
                always_ram=True
            )
        )
    )

    # Create a payload index for text field.
    # This index enables text search by the TEXT_FIELD_NAME field.
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

    # Upload points to the collection
    # Embeddings will be automatically generated from the Document model
    client.upload_points(
        collection_name=COLLECTION_NAME,
        points=tqdm(read_points()),
        parallel=4,
        batch_size=16,
    )


if __name__ == '__main__':
    upload_embeddings()
