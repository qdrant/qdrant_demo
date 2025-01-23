import os.path
from typing import Iterable

import pandas as pd
from qdrant_client import QdrantClient, models
from tqdm import tqdm

from qdrant_demo.config import DATA_DIR, QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME, TEXT_FIELD_NAME, EMBEDDINGS_MODEL

# Define the CSV file path and NPY file path
csv_file_path = os.path.join(DATA_DIR, "organizations.csv")


def read_points() -> Iterable[models.PointStruct]:
    df = pd.read_csv(csv_file_path)

    # Rename `short_description` to `document`
    df.rename(columns={"short_description": "document"}, inplace=True)

    for idx, row in df.iterrows():
        yield models.PointStruct(
            id=idx,
            vector=models.Document(
                text=row["document"],
                model=EMBEDDINGS_MODEL,
            ),
            payload=row.to_dict(),
        )


def upload_embeddings():
    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
    )

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
