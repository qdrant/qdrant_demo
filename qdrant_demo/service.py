import logging
import os


from fastapi import FastAPI

from qdrant_demo.config import COLLECTION_NAME
from qdrant_demo.neural_searcher import NeuralSearcher

app = FastAPI()
LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(level=LOGLEVEL)

searcher = NeuralSearcher(collection_name=COLLECTION_NAME)


@app.get("/search")
def read_item(q: str):
    return {
        "result": searcher.search(text=q)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
