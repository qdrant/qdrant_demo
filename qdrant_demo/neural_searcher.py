import json
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.http.models.models import Filter
from qdrant_client.models import VectorParams
from sentence_transformers import SentenceTransformer
from tqdm.notebook import tqdm

from backend import config


class NeuralSearcher:
    """A class for performing neural search using Qdrant and Sentence Transformers."""

    def __init__(self, collection_name: str, batch_size: int = 256, parallel: int = 2):
        self.collection_name = collection_name
        self.batch_size = batch_size
        self.parallel = parallel
        self.model = SentenceTransformer(
            config.QDRANT_ENCODER_MODEL,
            device=config.QDRANT_ENCODER_DEVICE,
        )
        self.qdrant_client = QdrantClient(
            host=config.QDRANT_HOST,
            port=config.QDRANT_PORT,
            prefer_grpc=True,
        )

    def search(self, text: str, filter_: Optional[Dict[str, Any]] = None) -> List[dict]:
        """Searches for relevant documents based on the given text.

        Args:
            text: The text to search for.
            filter_: Optional dictionary of filters to apply to the search.

        Returns:
            A list of dictionaries containing the search results.
        """
        if filter_ is None:
            filter_ = {}
        vector = self.model.encode(text).tolist()
        hits = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            query_filter=Filter(**filter_) if filter_ else None,
            top=5
        )
        return [hit.payload for hit in hits]

    @classmethod
    def covert_text_to_vector(cls, payload_json_file_path: str, output_vector_file_path: str) -> tuple:
        """Converts text to vectors using Sentence Transformers.

        Args:
            payload_json_file_path: Path to the JSON file containing the text payload.
            output_vector_file_path: Path to the output file where the vectors will be saved.

        Returns:
            A tuple containing the shape of the generated vectors.
        """
        model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens', device="cuda")
        df = pd.read_json(payload_json_file_path, lines=True)

        vectors = []
        batch_size = 64
        batch = []
        for row in tqdm(df.itertuples()):
            description = row.title + ". " + row.description
            batch.append(description)
            if len(batch) >= batch_size:
                vectors.append(model.encode(batch))
                batch = []

        if len(batch) > 0:
            vectors.append(model.encode(batch))
            batch = []

        vectors = np.concatenate(vectors)

        np.save(output_vector_file_path, vectors, allow_pickle=False)

        return vectors.shape

    @classmethod
    def upload_collection(cls, collection_name: str, payload_json_file_path: str, vector_file_path: str) -> bool:
        """Uploads a collection to Qdrant.

        This method uses a pre-trained sentence encoder (DistilBERT) for Semantic Textual Similarity.
        DistilBERT is a distilled (lightweight) version of the BERT model. For a full list of available
        models, visit https://www.sbert.net/docs/pretrained_models.html

        Args:
            collection_name: The name of the collection to upload.
            payload_json_file_path: Path to the JSON file containing the text payload.
            vector_file_path: Path to the file containing the vectors.

        Returns:
            True if the upload was successful, False otherwise.
        """
        vectors = np.load(vector_file_path)
        vector_size = vectors.shape[1]

        with open(payload_json_file_path) as fd:
            payload = list(map(json.loads, fd))

        self.qdrant_client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance="Cosine")
        )

        self.qdrant_client.upload_collection(
            collection_name=collection_name,
            vectors=vectors,
            payload=payload,
            ids=None,
            batch_size=self.batch_size,
            parallel=self.parallel
        )
        return True

    def is_healthy(self) -> bool:
        """Checks the health of the QdrantClient.

        Returns:
            True if the QdrantClient is healthy, False otherwise.
        """
        try:
            status = self.qdrant_client.status()
            return status["status"] == "ok"
        except Exception:
            return False
