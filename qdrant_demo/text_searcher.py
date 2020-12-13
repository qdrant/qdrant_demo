import os
import re

from qdrant_demo.config import DATA_DIR
from qdrant_demo.sqlite_searcher import SqliteSearch


class TextSearcher:
    def __init__(self):
        self.highlight_field = 'description'
        self.index = SqliteSearch(
            indexed_fields=['description'],
            path=os.path.join(DATA_DIR, 'startups.sqlite3'), is_read_only=True)

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

    def search(self, query, top=5):
        result = []
        for hit in self.index.search(query, limit=top):
            record = self.highlight(hit.record, query)
            result.append(record)
        return result