import json
import os
from typing import Iterable, List

import numpy as np

from qdrant_client import QdrantClient, models

from qdrant_demo.config import DATA_DIR, COLLECTION_NAME, QDRANT_HOST, QDRANT_PORT

BATCH_SIZE = 256


def mock_vectors(size, count) -> Iterable[List[float]]:
    for i in range(count):
        vector = np.random.rand(size).tolist()
        yield vector


if __name__ == '__main__':
    qdrant_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

    vector_size = 1

    payload_path = os.path.join(DATA_DIR, 'startups_uniq.json')
    with open(payload_path) as fd:
        payload = list(map(json.loads, fd))

    vectors = mock_vectors(vector_size, len(payload))

    qdrant_client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(size=vector_size, distance="Cosine")
    )

    qdrant_client.upload_collection(
        collection_name=COLLECTION_NAME,
        vectors=vectors,
        payload=payload,
        ids=None,
        batch_size=BATCH_SIZE,
        parallel=2
    )

    qdrant_client.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name="description",
        field_schema=models.TextIndexParams(
            type=models.TextIndexType.TEXT,
            tokenizer=models.TokenizerType.PREFIX,
            min_token_len=1,
            max_token_len=20,
            lowercase=True,
        )
    )
