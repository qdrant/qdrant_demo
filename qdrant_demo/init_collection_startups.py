import json
import os.path

import numpy as np
from qdrant_client import QdrantClient, models
from tqdm import tqdm

from qdrant_demo.config import DATA_DIR, QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME, TEXT_FIELD_NAME, VECTOR_FIELD_NAME

# Define the CSV file path and NPY file path
csv_file_path = os.path.join(DATA_DIR, "organizations.csv")
npy_file_path = os.path.join(DATA_DIR, "embeddings.npy")


def upload_embeddings():

    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        prefer_grpc=True,
    )

    vectors_path = os.path.join(DATA_DIR, 'startup_vectors.npy')
    vectors = np.load(vectors_path)
    vector_size = vectors.shape[1]

    payload_path = os.path.join(DATA_DIR, 'startups.json')
    payload = []

    with open(payload_path) as fd:
        for line in fd:
            obj = json.loads(line)
            # Rename fields to unified schema
            obj[TEXT_FIELD_NAME] = obj.pop('description')
            obj["logo_url"] = obj.pop("images")
            obj["homepage_url"] = obj.pop("link")
            payload.append(obj)

    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config={
            VECTOR_FIELD_NAME: models.VectorParams(
                size=vector_size,
                distance=models.Distance.COSINE,
                on_disk=True,
            )
        },
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

    client.upload_collection(
        collection_name=COLLECTION_NAME,
        vectors={
            VECTOR_FIELD_NAME: vectors
        },
        payload=payload,
        ids=None,  # Vector ids will be assigned automatically
        batch_size=64,  # How many vectors will be uploaded in a single request?
        parallel=10,
    )


if __name__ == '__main__':
    upload_embeddings()
