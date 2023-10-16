import os.path

import pandas as pd
from qdrant_client import QdrantClient, models
from tqdm import tqdm

from qdrant_demo.config import DATA_DIR, QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME, TEXT_FIELD_NAME, VECTOR_FIELD_NAME

# Define the CSV file path and NPY file path
csv_file_path = os.path.join(DATA_DIR, "organizations.csv")


def upload_embeddings():
    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
    )

    df = pd.read_csv(csv_file_path, nrows=1000)
    documents = df['short_description'].tolist()
    df.drop(columns=['short_description'], inplace=True)
    metadata = df.to_dict('records')

    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=client.get_fastembed_vector_params(on_disk=True),
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

    client.add(
        collection_name=COLLECTION_NAME,
        documents=documents,
        metadata=metadata,
        ids=tqdm(range(len(documents))),
        parallel=0,
    )


if __name__ == '__main__':
    upload_embeddings()
