import json
import os.path

from qdrant_client import QdrantClient, models
from qdrant_client.qdrant_fastembed import SUPPORTED_EMBEDDING_MODELS
from tqdm import tqdm

from qdrant_demo.config import DATA_DIR, QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME, TEXT_FIELD_NAME, \
    VECTOR_FIELD_NAME, EMBEDDINGS_MODEL


def upload_embeddings():
    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        prefer_grpc=True,
    )

    payload_path = os.path.join(DATA_DIR, 'startups.json')
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
        metadata=payload,
        ids=tqdm(range(len(payload))),
        parallel=0,
    )


if __name__ == '__main__':
    upload_embeddings()
