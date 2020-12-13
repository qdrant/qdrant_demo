import json
import pickle
import random
import re
import sqlite3
import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import Union, List, Iterable, Dict, Any

import pandas as pd
from loguru import logger


@dataclass
class SearchResult:
    record: dict
    score: float


class SqliteSearch:
    table_name = "search_table"

    escape_re = re.compile(r'[\W_]+', re.UNICODE)

    @classmethod
    def _make_or(cls, text: Union[str, list]):
        if isinstance(text, list):
            return " OR ".join([f"({cls._make_phrase(txt)})" for txt in text])
        return ' OR '.join(text.split())

    @classmethod
    def _make_and(cls, text: Union[str, list]):
        if isinstance(text, list):
            return " AND ".join([f"({cls._make_phrase(txt)})" for txt in text])
        return ' AND '.join(text.split())

    @classmethod
    def _make_phrase(cls, text):
        return ' + '.join(text.split())

    @classmethod
    def dict_factory(cls, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def __init__(self, indexed_fields: List[str], path: str, is_read_only=False):
        """
        :param indexed_fields: this fields will be added into database
        :param path: Path to database
        """
        self.is_read_only = is_read_only
        self.path = path
        self.indexed_fields = indexed_fields

        self.indexed_fields = self.indexed_fields

        self.connection = sqlite3.connect(path, check_same_thread=not is_read_only)
        self.connection.row_factory = self.dict_factory

        cursor = self.connection.cursor()

        fields = ", ".join(map(lambda x: f"{x}", self.indexed_fields))

        query = f'CREATE VIRTUAL TABLE IF NOT EXISTS {self.table_name} USING fts5({fields}' \
                f', record UNINDEXED, tokenize=porter);'

        cursor.execute(query)
        self.connection.commit()

    def index_record(self, record: dict):
        cursor = self.connection.cursor()

        query = f"INSERT INTO {self.table_name}({', '.join(self.indexed_fields)})" \
                f" VALUES({', '.join(['?'] * len(self.indexed_fields))})"

        cursor.execute(query, [record.get(field) for field in self.indexed_fields])
        self.connection.commit()

    def index_df(self, df: pd.DataFrame):
        records = [json.dumps(row._asdict()) for row in df.itertuples()]

        df = df[self.indexed_fields].copy()

        df['record'] = records

        df.to_sql(self.table_name, con=self.connection, if_exists='append', index=False)

        self.connection.commit()

    def clear_index(self):
        pass

    def save_index(self, path=None):
        path = path or (self.path + '.records.pkl')
        with open(path, 'wb') as out:
            pickle.dump(self.records, out)  # we do really need to preserve types here, so that is why use pickle
            # In other case is was easily to just store it in database

        return path

    def load_index(self, path=None):
        # Do not load any fields if we explicitly say so.
        # Should help with memory usage
        self.records_num_cache = self._record_length()

        if isinstance(self.record_fields, list) and not self.record_fields:
            self.records = None
            return

        path = path or (self.path + '.records.pkl')
        with open(path, 'rb') as fd:
            self.records = pickle.load(fd)

    def _escape_query(self, text):
        if isinstance(text, list):
            return [self._escape_query(txt) for txt in text]
        return re.sub(self.escape_re, ' ', text).lower()

    def _record_length(self) -> int:
        if self.records_num_cache is not None:
            return self.records_num_cache

        # Assume there were no deletions.
        query = f"SELECT MAX(_ROWID_) as cnt from {self.table_name} limit 1"
        cursor = self.connection.cursor()
        cursor.execute(query)
        res = cursor.fetchone()
        if res['cnt'] is None:
            self.records_num_cache = 0
        else:
            self.records_num_cache = res['cnt']
        return self.records_num_cache

    def _get_record(self, idx: int) -> Dict[str, Any]:
        res = {}
        if self.records is None:
            return {}
        for field in self.records:
            res[field] = self.records[field][idx]
        return res

    def _append_record(self, record: dict):
        if len(record) == 0:
            return
        for key, val in record.items():
            self.records[key].append(val)

    def get_record_by_id(self, idx) -> SearchResult:
        rowid = idx + 1
        cur = self.connection.cursor()
        cur.execute('SELECT * FROM search_table where rowid = ?', (rowid,))
        res = cur.fetchone()
        cur.close()

        return SearchResult(
            record=self._get_record(res['index']),
            score=0.0,
        )

    def get_random(self) -> SearchResult:
        rand_id = random.randint(0, self._record_length() - 1)
        return self.get_record_by_id(rand_id)

    def all_records(self) -> Iterable[SearchResult]:
        for idx in range(0, self._record_length()):
            yield self.get_record_by_id(idx)

    def _execute_query(
            self,
            search_query: str,
            conditions: str,
    ) -> List[SearchResult]:

        cursor = self.connection.cursor()
        try:
            cursor.execute(search_query, [conditions])
            data = cursor.fetchall()
        except sqlite3.OperationalError as e:
            logger.error(f"Failed to execute: {e}", exc_info=sys.exc_info())
            logger.error(f"Failed query: {search_query}, conditions {conditions}")
            data = []

        result = []
        for row in data:
            res_row = SearchResult(
                record=json.loads(row['record']),
                score=-row['rank'],
            )
            result.append(res_row)

        return result

    def _get_search_query(self, return_fields: List[str], limit: int, order: bool):
        return_fields_sql = ", ".join(map(lambda x: f'"{x}"', return_fields))

        order_query = "ORDER BY rank" if order else ""

        search_query = f"SELECT {return_fields_sql}, record, rank " \
                       f"FROM {self.table_name} WHERE {self.table_name} MATCH ? " \
                       f"{order_query} LIMIT {limit}"
        return search_query

    def search(
            self,
            query: str,
            limit: int,
            order: bool = True,
    ) -> List[SearchResult]:

        return_fields = self.indexed_fields

        query = self._escape_query(query)

        conditions = f" OR ".join(f"{field}:({self._make_or(query)})" for field in self.indexed_fields)

        search_query = self._get_search_query(return_fields, limit, order)

        return self._execute_query(search_query, conditions)
