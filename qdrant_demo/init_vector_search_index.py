import json
import os

from qdrant_demo.config import DATA_DIR, COLLECTION_NAME
from qdrant_demo.neural_searcher import NeuralSearcher

BATCH_SIZE = 256


if __name__ == '__main__':
    neural_searcher = NeuralSearcher(COLLECTION_NAME)
    payload_path = os.path.join(DATA_DIR, 'web_summit_startups.jsonl')

    with open(payload_path) as fd:
        payload = list(map(json.loads, fd))

    vectors = neural_searcher.model.encode([record['description'] for record in payload])

    neural_searcher.qdrant_client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vector_size=neural_searcher.model.get_sentence_embedding_dimension()
    )

    neural_searcher.qdrant_client.upload_collection(
        collection_name=COLLECTION_NAME,
        vectors=vectors,
        payload=payload,
        ids=None,
        batch_size=BATCH_SIZE,
        parallel=2
    )
