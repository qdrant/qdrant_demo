"""Build the startups collection the search path expects: a named `dense` vector
(mxbai) plus a `sparse` bm25 keyword vector with IDF, and a text index for keyword
search. Payload fields are renamed once here to the schema the frontend reads
(`document`, `logo_url`, `homepage_url`). Both vectors are embedded through
`models.Document` (server-side with Cloud inference, or client-side with fastembed
when CLOUD_INFERENCE=0), so the query and document sides use the identical models.
Documents get no mxbai prefix; the query prefix is added at search time.
Run:  python -m qdrant_demo.init_collection_startups
"""
import json
import os
from typing import Iterable

from qdrant_client import QdrantClient, models
from tqdm import tqdm

from qdrant_demo.config import (
    DATA_DIR, QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME, TEXT_FIELD_NAME,
    EMBEDDINGS_MODEL, SPARSE_EMBEDDINGS_MODEL, DENSE_VECTOR_NAME, SPARSE_VECTOR_NAME,
    CLOUD_INFERENCE,
)

DENSE_DIM = 1024  # mxbai-embed-large-v1


def _prepare(obj: dict) -> dict:
    # Rename to the unified schema the frontend and search path read.
    obj["logo_url"] = obj.pop("images", None)
    obj["homepage_url"] = obj.pop("link", None)
    obj[TEXT_FIELD_NAME] = obj.pop("description", "")
    return obj


def _records() -> Iterable[dict]:
    path = os.path.join(DATA_DIR, "startups_demo.json")
    with open(path, encoding="utf-8") as fd:
        for line in fd:
            line = line.strip()
            if line:
                yield _prepare(json.loads(line))


def _doc_text(obj: dict) -> str:
    # The exact text all three modes see: the same `document` field the keyword
    # index is built on. Keeping them identical is what makes the mode comparison
    # honest, so dense, sparse, and keyword match on the same string.
    return obj.get(TEXT_FIELD_NAME, "") or ""


def build():
    # cloud_inference=True embeds server-side (Qdrant Cloud). With it False and the
    # fastembed extra installed, the same models.Document calls embed client-side,
    # so this script also works against a local OSS container.
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, cloud_inference=CLOUD_INFERENCE)

    if client.collection_exists(COLLECTION_NAME):
        print(f"{COLLECTION_NAME} exists, recreating.")
        client.delete_collection(COLLECTION_NAME)

    client.create_collection(
        COLLECTION_NAME,
        vectors_config={
            DENSE_VECTOR_NAME: models.VectorParams(
                size=DENSE_DIM, distance=models.Distance.COSINE, on_disk=True,
            )
        },
        sparse_vectors_config={
            # bm25 values carry term frequency; IDF is applied at query time.
            SPARSE_VECTOR_NAME: models.SparseVectorParams(modifier=models.Modifier.IDF)
        },
        quantization_config=models.ScalarQuantization(
            scalar=models.ScalarQuantizationConfig(
                type=models.ScalarType.INT8, quantile=0.99, always_ram=True,
            )
        ),
    )
    client.create_payload_index(
        COLLECTION_NAME, field_name=TEXT_FIELD_NAME,
        field_schema=models.TextIndexParams(
            type=models.TextIndexType.TEXT, tokenizer=models.TokenizerType.WORD,
            min_token_len=2, max_token_len=20, lowercase=True,
        ),
    )

    def points() -> Iterable[models.PointStruct]:
        for idx, obj in enumerate(_records()):
            text = _doc_text(obj)
            yield models.PointStruct(
                id=idx,
                vector={
                    DENSE_VECTOR_NAME: models.Document(text=text, model=EMBEDDINGS_MODEL),
                    SPARSE_VECTOR_NAME: models.Document(text=text, model=SPARSE_EMBEDDINGS_MODEL),
                },
                payload=obj,
            )

    client.upload_points(COLLECTION_NAME, points=tqdm(points()), batch_size=64)
    print(f"built {COLLECTION_NAME}: {client.count(COLLECTION_NAME).count} points")


if __name__ == "__main__":
    build()
