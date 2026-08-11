import os

CODE_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(CODE_DIR)
DATA_DIR = os.path.join(ROOT_DIR, "data")
STATIC_DIR = os.path.join(ROOT_DIR, "static")

QDRANT_URL = os.environ.get("QDRANT_URL", "http://localhost:6333/")
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY", "")

# `or` rather than a get() default: a missing deploy secret expands to an empty
# string, which is set-but-useless, and every request would 502 on a nameless
# collection instead of falling back here.
COLLECTION_NAME = os.environ.get("COLLECTION_NAME") or "startups_hybrid_v2"
EMBEDDINGS_MODEL = os.environ.get("EMBEDDINGS_MODEL", "mixedbread-ai/mxbai-embed-large-v1")
# Sparse keyword model. Qdrant/bm25 handles tokenization, stemming, and stopwords;
# IDF is applied server-side via the collection's sparse modifier.
SPARSE_EMBEDDINGS_MODEL = os.environ.get("SPARSE_EMBEDDINGS_MODEL", "Qdrant/bm25")

TEXT_FIELD_NAME = os.environ.get("TEXT_FIELD_NAME", "document")

# Named vectors on the hybrid collection. Leave DENSE_VECTOR_NAME empty for a
# collection with a single unnamed vector.
DENSE_VECTOR_NAME = os.environ.get("DENSE_VECTOR_NAME", "dense")
SPARSE_VECTOR_NAME = os.environ.get("SPARSE_VECTOR_NAME", "sparse")

# Embed the query with Qdrant Cloud server-side inference. Defaults ON: the query
# model is a 1024-d mxbai, too heavy to embed per-request on a small CPU box.
# Parse leniently since some hosts keep the surrounding quotes on the value.
CLOUD_INFERENCE = os.environ.get("CLOUD_INFERENCE", "1").strip().strip('"').strip("'").lower() in ("1", "true", "yes")
RESULT_LIMIT = int(os.environ.get("RESULT_LIMIT", "20"))
# Candidates each half of the hybrid query fetches before RRF. At 2x the result
# limit the two lists barely intersect on a 3M collection, so fusion degrades to
# interleaving. 10x measured 3x to 6x more shared documents for +4 ms at p50.
HYBRID_PREFETCH = int(os.environ.get("HYBRID_PREFETCH", "200"))
