import json
import os
import numpy as np

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams

from qdrant_demo.config import DATA_DIR, COLLECTION_NAME, QDRANT_HOST, QDRANT_PORT

BATCH_SIZE = 256


if __name__ == '__main__':
    qdrant_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

    vectors_path = os.path.join(DATA_DIR, 'startup_vectors.npy')
    vectors = np.load(vectors_path)
    vector_size = vectors.shape[1]

    payload_path = os.path.join(DATA_DIR, 'startups.json')
    with open(payload_path) as fd:
        payload = list(map(json.loads, fd))

    qdrant_client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=vector_size, distance="Cosine")
    )

    qdrant_client.upload_collection(
        collection_name=COLLECTION_NAME,
        vectors=vectors,
        payload=payload,
        ids=None,
        batch_size=BATCH_SIZE,
        parallel=2
    )
