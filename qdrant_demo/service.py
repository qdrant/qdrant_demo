import os
import logging
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

from qdrant_demo.config import (
    COLLECTION_NAME, STATIC_DIR, RESULT_LIMIT, CLOUD_INFERENCE, EMBEDDINGS_MODEL,
)
from qdrant_demo.neural_searcher import NeuralSearcher
from qdrant_demo.text_searcher import TextSearcher

from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

neural_searcher = NeuralSearcher(collection_name=COLLECTION_NAME)
text_searcher = TextSearcher(collection_name=COLLECTION_NAME)


@app.get("/api/search")
async def read_item(q: str, mode: Optional[str] = None, neural: Optional[bool] = None):
    """mode = semantic (dense) | keyword (full-text) | hybrid (dense + keyword).

    Back-compat with the older frontend, which passes `neural` (bool):
    neural=true -> semantic (its original meaning), neural=false -> keyword.
    When neither is given, default to hybrid. Explicit `mode` always wins."""
    if mode is None:
        mode = "semantic" if neural is True else "keyword" if neural is False else "hybrid"
    if mode not in ("semantic", "keyword", "hybrid"):
        raise HTTPException(status_code=400, detail=f"unknown mode: {mode}")
    if not q.strip():
        return {"result": [], "stats": {"mode": mode}}
    try:
        if mode == "keyword":
            return {"result": text_searcher.search(query=q, top=RESULT_LIMIT),
                    "stats": {"mode": "keyword"}}
        out = neural_searcher.search(text=q, hybrid=(mode == "hybrid"))
        return {"result": out["results"], "stats": out["stats"]}
    except Exception as e:
        logger.exception("search failed for q=%r mode=%s", q, mode)
        raise HTTPException(status_code=502, detail="Search is temporarily unavailable.")


@app.get("/api/stats")
async def stats():
    """Live collection size, so the frontend can show off the scale."""
    try:
        count = neural_searcher.qdrant_client.count(COLLECTION_NAME).count
        return {
            "count": count, "collection": COLLECTION_NAME,
            "cloud_inference": CLOUD_INFERENCE, "model": EMBEDDINGS_MODEL,
        }
    except Exception:
        logger.exception("stats failed")
        raise HTTPException(status_code=502, detail="Stats are temporarily unavailable.")


# Mount the static files directory once the search endpoint is defined
if os.path.exists(STATIC_DIR):
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
