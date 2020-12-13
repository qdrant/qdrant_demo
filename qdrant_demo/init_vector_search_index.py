import json
import logging
import os
from itertools import islice
from typing import Iterable

import numpy as np
from qdrant_openapi_client.model.point_struct import PointStruct
from tqdm import tqdm

from qdrant_demo.config import COLLECTION_NAME, DATA_DIR
from qdrant_demo.qdrant_client import QdrantClient

BATCH_SIZE = 256


def iter_batch(iterable, size):
    """
    >>> list(iter_batch([1,2,3,4,5], 3))
    [[1, 2, 3], [4, 5]]

    """
    source_iter = iter(iterable)
    while source_iter:
        b = list(islice(source_iter, size))
        if len(b) == 0:
            break
        yield b


class VectorUploader:
    def __init__(self):
        self.qdrant_client = QdrantClient()

    def read_points(self, data: Iterable[dict], vectors: np.ndarray) -> Iterable[PointStruct]:
        for idx, (record, vector) in tqdm(enumerate(zip(data, vectors))):
            yield self.qdrant_client.make_point(idx=idx, vector=vector.tolist(), payload=record)

    def upload_to_qdrant(self, data: Iterable[dict], vectors: np.ndarray):
        vector_size = vectors.shape[1]
        self.qdrant_client.recreate_collection(COLLECTION_NAME, vector_size=vector_size)

        for point_batch in iter_batch(self.read_points(data, vectors), BATCH_SIZE):
            self.qdrant_client.upload_point(COLLECTION_NAME, points=point_batch)

    def read_and_upload(self, payload_path: str, vectors_path: str):
        vectors = np.load(vectors_path)
        with open(payload_path) as fd:
            data = map(json.loads, fd)
            self.upload_to_qdrant(data, vectors)


if __name__ == '__main__':
    LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
    logging.basicConfig(level=LOGLEVEL)
    uploader = VectorUploader()
    uploader.read_and_upload(
        payload_path=os.path.join(DATA_DIR, 'startups.json'),
        vectors_path=os.path.join(DATA_DIR, 'startup_vectors.npy')
    )

