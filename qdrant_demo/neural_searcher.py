from typing import List

from qdrant_client import QdrantClient
from qdrant_client.http.models.models import Filter

from qdrant_demo.config import QDRANT_URL, QDRANT_API_KEY


class NeuralSearcher:

    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

    def search(self, text: str, filter_: dict = None) -> List[dict]:
        hits = self.qdrant_client.query(
            collection_name=self.collection_name,
            query_text=text,
            query_filter=Filter(**filter_) if filter_ else None,
            limit=5
        )
        return [hit.metadata for hit in hits]
