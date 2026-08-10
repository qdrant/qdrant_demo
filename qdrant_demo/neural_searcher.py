import os
import time
import logging

from qdrant_client import QdrantClient, models

from qdrant_demo.config import (
    QDRANT_URL, QDRANT_API_KEY, EMBEDDINGS_MODEL, SPARSE_EMBEDDINGS_MODEL,
    DENSE_VECTOR_NAME, SPARSE_VECTOR_NAME, RESULT_LIMIT, HYBRID_PREFETCH,
    CLOUD_INFERENCE,
)

logger = logging.getLogger(__name__)


class NeuralSearcher:
    """Dense (semantic) and hybrid (dense + bm25 keyword, fused with RRF) search
    over a collection with a named dense vector and a bm25 sparse vector."""

    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        # Fail loudly instead of hanging: measured novel-query latency is well
        # under a second, so 15s is a generous ceiling that still surfaces a real
        # problem quickly rather than masking it for a minute.
        timeout = int(os.environ.get("QDRANT_TIMEOUT", "15"))
        self.qdrant_client = QdrantClient(
            url=QDRANT_URL, api_key=QDRANT_API_KEY, prefer_grpc=True,
            cloud_inference=CLOUD_INFERENCE, timeout=timeout,
        )

    # mxbai is an asymmetric retrieval model: the query gets a prompt prefix, the
    # stored documents do not, so applying it only here needs no re-indexing.
    # Qdrant Cloud inference already applies this prompt server-side, so on the
    # Cloud path the prefix is a verified no-op (identical scores). It matters for
    # the self-hosted / local-embedding path, where nothing else adds it.
    QUERY_PREFIX = "Represent this sentence for searching relevant passages: "

    def _dense(self, text: str):
        return models.Document(text=self.QUERY_PREFIX + text, model=EMBEDDINGS_MODEL)

    def _sparse(self, text: str):
        return models.Document(text=text, model=SPARSE_EMBEDDINGS_MODEL)

    def _dense_only(self, text: str):
        return self.qdrant_client.query_points(
            collection_name=self.collection_name,
            query=self._dense(text),
            using=DENSE_VECTOR_NAME or None,
            limit=RESULT_LIMIT,
        ).points

    def search(self, text: str, hybrid: bool = False) -> dict:
        t0 = time.perf_counter()
        mode = "hybrid" if hybrid else "semantic"

        if hybrid:
            hits = self.qdrant_client.query_points(
                collection_name=self.collection_name,
                prefetch=[
                    models.Prefetch(query=self._dense(text), using=DENSE_VECTOR_NAME or None, limit=HYBRID_PREFETCH),
                    models.Prefetch(query=self._sparse(text), using=SPARSE_VECTOR_NAME, limit=HYBRID_PREFETCH),
                ],
                query=models.FusionQuery(fusion=models.Fusion.RRF),
                limit=RESULT_LIMIT,
            ).points
        else:
            hits = self._dense_only(text)

        results = [{**hit.payload, "score": hit.score} for hit in hits]
        # Timing stays server-side for debugging; it's not returned to the client.
        # This is a relevance demo, not a benchmark.
        logger.debug("%s search took %d ms", mode, round((time.perf_counter() - t0) * 1000))
        stats = {
            "mode": mode,
            "embedding_model": EMBEDDINGS_MODEL,
            # Hybrid returns a rank-fusion score, semantic a cosine similarity.
            # Both land in 0..1 but mean different things, so label which one.
            "score_type": "rrf" if mode == "hybrid" else "cosine",
            "results": len(results),
        }
        return {"results": results, "stats": stats}
