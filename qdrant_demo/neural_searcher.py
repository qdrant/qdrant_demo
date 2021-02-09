import logging
import os
from typing import List

import psutil
from qdrant_client import QdrantClient
from qdrant_openapi_client.models.models import Filter
from sentence_transformers import SentenceTransformer


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

    def search(self, text: str, filter_: dict = None) -> List[dict]:
        vector = self.model.encode(text).tolist()
        search_result = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            query_filter=Filter(**filter_) if filter_ else None,
            top=5
        )
        payloads = [payload for point, payload in search_result]
        return payloads
