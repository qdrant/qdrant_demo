from typing import List

from qdrant_client import QdrantClient
from qdrant_client.http.models.models import Filter
from sentence_transformers import SentenceTransformer

from qdrant_demo_v2.config import QDRANT_URL, QDRANT_API_KEY


class NeuralSearcher:

    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

    def search(self, text: str, filter_: dict = None) -> List[dict]:
        vector = self.model.encode(text).tolist()
        hits = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=("fast-bge-small-en", vector),
        
            query_filter=Filter(**filter_) if filter_ else None,
            limit=5
        )
        return [hit.payload for hit in hits]
