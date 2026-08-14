import os
import re

from qdrant_client import QdrantClient, models

from qdrant_demo.config import (
    QDRANT_URL, QDRANT_API_KEY, TEXT_FIELD_NAME, SPARSE_EMBEDDINGS_MODEL,
    SPARSE_VECTOR_NAME, RESULT_LIMIT, CLOUD_INFERENCE,
)


class TextSearcher:
    """Keyword search over the bm25 sparse vector.

    Queries the same sparse vector the hybrid prefetch uses, so results come back
    ranked by bm25 with IDF applied server-side by the collection's sparse
    modifier. A payload MatchText filter would only answer "does this document
    contain every term", which returns an unordered subset.
    """

    def __init__(self, collection_name: str):
        self.highlight_field = TEXT_FIELD_NAME
        self.collection_name = collection_name
        timeout = int(os.environ.get("QDRANT_TIMEOUT", "15"))
        self.qdrant_client = QdrantClient(
            url=QDRANT_URL, api_key=QDRANT_API_KEY, prefer_grpc=True,
            cloud_inference=CLOUD_INFERENCE, timeout=timeout,
        )

    def highlight(self, record, query) -> dict:
        text = record[self.highlight_field]

        for word in query.lower().split():
            if len(word) > 4:
                pattern = re.compile(fr"(\b{re.escape(word)}?.?\b)", flags=re.IGNORECASE)
            else:
                pattern = re.compile(fr"(\b{re.escape(word)}\b)", flags=re.IGNORECASE)
            text = re.sub(pattern, r"<b>\1</b>", text)

        record[self.highlight_field] = text
        return record

    def search(self, query, top=RESULT_LIMIT):
        hits = self.qdrant_client.query_points(
            collection_name=self.collection_name,
            query=models.Document(text=query, model=SPARSE_EMBEDDINGS_MODEL),
            using=SPARSE_VECTOR_NAME,
            limit=top,
        ).points
        # bm25 scores are unbounded, unlike the cosine and RRF scores the other
        # modes return. /api/search labels the scale as "bm25" so the client knows.
        return [{**self.highlight(hit.payload, query), "score": hit.score} for hit in hits]
