import json
import logging
import os
from itertools import islice
from typing import Iterable

import numpy as np
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


def upload_to_qdrant(data: Iterable[dict], vectors: np.ndarray):
    qdrant_client = QdrantClient()
    vector_size = vectors.shape[1]
    qdrant_client.recreate_collection(COLLECTION_NAME, vector_size=vector_size)
    points = []
    for idx, (record, vector) in tqdm(enumerate(zip(data, vectors))):
        points.append(qdrant_client.make_point(idx=idx, vector=vector.tolist(), payload=record))
        if len(points) >= BATCH_SIZE:
            qdrant_client.upload_point(COLLECTION_NAME, points=points)
            points = []
    if len(points) > 0:
        qdrant_client.upload_point(COLLECTION_NAME, points=points)


if __name__ == '__main__':
    LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
    logging.basicConfig(level=LOGLEVEL)
    vectors_ = np.load(os.path.join(DATA_DIR, 'startup_vectors.npy'))
    data_ = map(json.loads, open(os.path.join(DATA_DIR, 'startups.json')))

    upload_to_qdrant(data_, vectors_)
