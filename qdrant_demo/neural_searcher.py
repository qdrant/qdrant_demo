import time
from typing import List

from qdrant_client import QdrantClient
from qdrant_client.http.models.models import Filter

from qdrant_demo.config import QDRANT_URL, QDRANT_API_KEY, EMBEDDINGS_MODEL


class NeuralSearcher:

    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, prefer_grpc=True)
        self.qdrant_client.set_model(EMBEDDINGS_MODEL)

    def search(self, text: str, filter_: dict = None) -> List[dict]:
        start_time = time.time()
        hits = self.qdrant_client.query(
            collection_name=self.collection_name,
            query_text=text,
            query_filter=Filter(**filter_) if filter_ else None,
            limit=5
        )
        print(f"Search took {time.time() - start_time} seconds")
        return [hit.metadata for hit in hits]
