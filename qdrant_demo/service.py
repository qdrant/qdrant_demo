from fastapi import FastAPI

from qdrant_demo.config import COLLECTION_NAME
from qdrant_demo.neural_searcher import NeuralSearcher
from qdrant_demo.text_searcher import TextSearcher

app = FastAPI()

neural_searcher = NeuralSearcher(collection_name=COLLECTION_NAME)
text_searcher = TextSearcher()


@app.get("/api/search")
async def read_item(q: str, neural: bool = True):
    return {
        "result": neural_searcher.search(text=q)
        if neural else text_searcher.search(query=q)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
