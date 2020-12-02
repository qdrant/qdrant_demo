import logging
import os
from typing import List, Optional

import psutil
from qdrant_openapi_client.model_utils import validate_and_convert_types
from sentence_transformers import SentenceTransformer

from qdrant_demo.qdrant_client import QdrantClient
from qdrant_openapi_client.model.filter import Filter
from qdrant_openapi_client.model.scored_point import ScoredPoint


class NeuralSearcher:

    @classmethod
    def load_model(cls, device=None):
        model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens', device=device)  # , device="cpu"
        process = psutil.Process(os.getpid())
        used_mem_mb = process.memory_info().rss / 1024 / 1024
        logging.info(f"Memory usage: {used_mem_mb} Mb")
        return model

    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.model = self.load_model(device='cpu')
        self.qdrant_client = QdrantClient()

    @classmethod
    def _convert_filters(cls, filter_: dict) -> Optional[Filter]:
        if not filter_:
            return None

        return Filter(**filter_)

    def search(self, text: str, filter_: dict = None) -> List[dict]:
        vector = self.model.encode(text).tolist()
        res: List[ScoredPoint] = self.qdrant_client.search(
            collection_name=self.collection_name,
            vector=vector,
            filter_=filter_
        ).result

        payloads = self.qdrant_client.lookup(self.collection_name, [point.id for point in res])

        return payloads

