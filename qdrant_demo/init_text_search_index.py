import os
from typing import List

import pandas as pd

from qdrant_demo.config import DATA_DIR
from qdrant_demo.sqlite_searcher import SqliteSearch


class TextIndexing:

    def __init__(self, index_path: str, indexed_fields: List[str]):
        self.searcher = SqliteSearch(indexed_fields, index_path)

    def index(self, data_path: str):
        df = pd.read_json(data_path, lines=True)
        df.drop_duplicates(inplace=True)
        self.searcher.index_df(df)


if __name__ == '__main__':
    index_path = os.path.join(DATA_DIR, 'startups.sqlite3')
    if os.path.exists(index_path):
        os.remove(index_path)
    indexer = TextIndexing(index_path, indexed_fields=["description", 'name'])
    indexer.index(os.path.join(DATA_DIR, 'startups.json'))

    search_test = indexer.searcher.search(query="cyber sport", limit=5)
    for res in search_test:
        print(res)
