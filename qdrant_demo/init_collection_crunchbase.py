"""Build a larger startups collection from the Crunchbase organizations.csv, with
the same schema the search path expects: a named `dense` (mxbai) vector plus a
`sparse` bm25 vector with IDF, and a text index on `document`. Mirrors
init_collection_startups so the app can query either collection unchanged.
Run:  python -m qdrant_demo.init_collection_crunchbase
"""
import os.path
from typing import Iterable

import pandas as pd
from qdrant_client import QdrantClient, models
from tqdm import tqdm

from qdrant_demo.config import (
    DATA_DIR, QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME, TEXT_FIELD_NAME,
    EMBEDDINGS_MODEL, SPARSE_EMBEDDINGS_MODEL, DENSE_VECTOR_NAME, SPARSE_VECTOR_NAME,
    CLOUD_INFERENCE,
)

csv_file_path = os.path.join(DATA_DIR, "organizations.csv")
DENSE_DIM = 1024  # mxbai-embed-large-v1


def read_points() -> Iterable[models.PointStruct]:
    df = pd.read_csv(csv_file_path)
    df.rename(columns={"short_description": TEXT_FIELD_NAME}, inplace=True)
    for idx, row in df.iterrows():
        text = str(row.get(TEXT_FIELD_NAME) or "")
        yield models.PointStruct(
            id=idx,
            vector={
                DENSE_VECTOR_NAME: models.Document(text=text, model=EMBEDDINGS_MODEL),
                SPARSE_VECTOR_NAME: models.Document(text=text, model=SPARSE_EMBEDDINGS_MODEL),
            },
            payload=row.to_dict(),
        )


def upload_embeddings():
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, cloud_inference=CLOUD_INFERENCE)

    if client.collection_exists(COLLECTION_NAME):
        print(f"Collection {COLLECTION_NAME} already exists. Remove it first.")
        client.delete_collection(COLLECTION_NAME)

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config={
            DENSE_VECTOR_NAME: models.VectorParams(
                size=DENSE_DIM, distance=models.Distance.COSINE, on_disk=True,
            )
        },
        sparse_vectors_config={
            SPARSE_VECTOR_NAME: models.SparseVectorParams(modifier=models.Modifier.IDF)
        },
        quantization_config=models.ScalarQuantization(
            scalar=models.ScalarQuantizationConfig(
                type=models.ScalarType.INT8, quantile=0.99, always_ram=True,
            )
        ),
    )
    client.create_payload_index(
        collection_name=COLLECTION_NAME, field_name=TEXT_FIELD_NAME,
        field_schema=models.TextIndexParams(
            type=models.TextIndexType.TEXT, tokenizer=models.TokenizerType.WORD,
            min_token_len=2, max_token_len=20, lowercase=True,
        ),
    )

    client.upload_points(COLLECTION_NAME, points=tqdm(read_points()), batch_size=64)
    print(f"built {COLLECTION_NAME}: {client.count(COLLECTION_NAME).count} points")


if __name__ == '__main__':
    upload_embeddings()
