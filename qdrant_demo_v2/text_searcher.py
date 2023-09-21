import os
import re

from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchText
from qdrant_demo_v2.config import QDRANT_URL, QDRANT_API_KEY



class TextSearcher:
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)


    def search(self, query, top=5):
        hits = self.qdrant_client.scroll(
        collection_name=self.collection_name,
        scroll_filter=Filter(
            must=[ 
                FieldCondition(
                key='short_description',  
                match=MatchText(text=query),
            )
        ]),
            with_payload=True,
            with_vectors=False,
            limit=top
        )
        return [hit.payload for hit in hits[0]]

        
