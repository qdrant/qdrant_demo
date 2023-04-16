import json
import os
from typing import Any, Dict, List, Optional

import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.http.models.models import Filter
from qdrant_client.models import VectorParams
from sentence_transformers import SentenceTransformer

from backend import config


class NeuralSearcher:
    """A class for performing neural search using Qdrant and Sentence Transformers."""

    def __init__(self, collection_name: str, batch_size: int = 256, parallel: int = 2):
        self.collection_name = collection_name
        self.batch_size = batch_size
        self.parallel = parallel
        self.model = SentenceTransformer(
            config.QDRANT_ENCODER_MODEL, 
            device=config.QDRANT_ENCODER_DEVICE,
        )
        self.qdrant_client = QdrantClient(
            host=config.QDRANT_HOST, 
            port=config.QDRANT_PORT,
        )

    def search(self, text: str, filter_: Optional[Dict[str, Any]] = None) -> List[dict]:
        """Searches for relevant documents based on the given text."""
        if filter_ is None:
            filter_ = {}
        vector = self.model.encode(text).tolist()
        hits = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            query_filter=Filter(**filter_) if filter_ else None,
            top=5
        )
        return [hit.payload for hit in hits]

    def upload_collection(self, collection_name: str, payload_file_path: str, vectors_path: str) -> bool:
        """Uploads a collection to Qdrant."""
        vectors = np.load(vectors_path)
        vector_size = vectors.shape[1]

        with open(payload_file_path) as fd:
            payload = list(map(json.loads, fd))

        self.qdrant_client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance="Cosine")
        )

        self.qdrant_client.upload_collection(
            collection_name=collection_name,
            vectors=vectors,
            payload=payload,
            ids=None,
            batch_size=self.batch_size,
            parallel=self.parallel
        )

    def is_healthy(self) -> bool:
        """Checks the health of the QdrantClient."""
        try:
            status = self.qdrant_client.status()
            return status["status"] == "ok"
        except Exception:
            return False
