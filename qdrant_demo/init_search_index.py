import csv
import logging
import os
from itertools import islice
from typing import Iterable, Dict

import nltk
import psutil
from nltk import tokenize
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

from qdrant_demo.config import DATA_DIR, COLLECTION_NAME
from qdrant_demo.neural_searcher import NeuralSearcher
from qdrant_demo.qdrant_client import QdrantClient

BATCH_SIZE = 32


def iter_batch(iterable, size):
    """
    >>> list(iter_batch([1,2,3,4,5], 3))
    [[1, 2, 3], [4, 5]]

    """
    source_iter = iter(iterable)
    while source_iter:
        b = list(islice(source_iter, size))
        if len(b) == 0:
            break
        yield b


def iterate_books_data(data_path) -> Iterable[dict]:
    with open(data_path) as fd:
        csv_reader = csv.DictReader(fd)
        for row in csv_reader:
            yield {
                "book_id": int(row["id"]),
                "authors": row["authors"],
                "year": int(float(row["original_publication_year"])) if row["original_publication_year"] else None,
                "title": row["title"],
                "rating": float(row["average_rating"]),
                "image_url": row["small_image_url"],
                "description": row["description"]
            }


def split_sentences(books: Iterable[dict]) -> Iterable[dict]:
    for book in books:
        description = book.get('description')
        sentences = tokenize.sent_tokenize(description)
        for sentence_id, sentence in enumerate(sentences):
            if len(sentence) < 5:
                continue
            yield {
                **book,
                "sentence": sentence,
                "sentence_id": sentence_id
            }


def upload_data_to_search(data: Iterable[dict], vectorized_field):
    qdrant_client = QdrantClient()
    model = NeuralSearcher.load_model()
    vector_size = model.get_sentence_embedding_dimension()
    qdrant_client.recreate_collection(COLLECTION_NAME, vector_size=vector_size)
    num = 0
    for batch in tqdm(iter_batch(data, BATCH_SIZE)):
        embeddings_batch = model.encode([row[vectorized_field] for row in batch], show_progress_bar=False)
        points = []
        for vec, row in zip(embeddings_batch, batch):
            points.append(qdrant_client.make_point(idx=num, vector=vec.tolist(), payload=row))
            num += 1

        qdrant_client.upload_point(COLLECTION_NAME, points=points)

        # if num > 250:
        #     break


if __name__ == '__main__':
    LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
    logging.basicConfig(level=LOGLEVEL)
    nltk.download('punkt')
    books_path = os.path.join(DATA_DIR, 'top2k_book_descriptions.csv')
    books = iterate_books_data(books_path)
    upload_data_to_search(split_sentences(books), vectorized_field="sentence")
