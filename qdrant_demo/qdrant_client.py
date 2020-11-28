import os
from typing import Dict, List

import qdrant_openapi_client
from qdrant_openapi_client.api.collections_api import CollectionsApi
from qdrant_openapi_client.api.points_api import PointsApi
from qdrant_openapi_client.model.collection_update_operations import CollectionUpdateOperations
from qdrant_openapi_client.model.distance import Distance
from qdrant_openapi_client.model.payload_interface import PayloadInterface
from qdrant_openapi_client.model.point_insert_ops import PointInsertOps
from qdrant_openapi_client.model.point_struct import PointStruct
from qdrant_openapi_client.model.storage_ops import StorageOps
from qdrant_openapi_client.model.storage_ops_any_of_create_collection import StorageOpsAnyOfCreateCollection

QDRANT_HOST = os.environ.get("QDRANT_HOST", "localhost")
QDRANT_PORT = os.environ.get("QDRANT_PORT", 6333)


class QdrantClient:

    @classmethod
    def _get_qdrant_client(cls):
        configuration = qdrant_openapi_client.Configuration(
            host=f"http://{QDRANT_HOST}:{QDRANT_PORT}"
        )
        api_client = qdrant_openapi_client.ApiClient(configuration)
        return api_client

    @classmethod
    def _get_collection_api(cls):
        api_client = cls._get_qdrant_client()
        collections_api = CollectionsApi(api_client)
        return collections_api

    @classmethod
    def _get_points_api(cls):
        api_client = cls._get_qdrant_client()
        points_api = PointsApi(api_client)
        return points_api

    def __init__(self):
        self.collection_api = self._get_collection_api()
        self.point_api = self._get_points_api()

    def recreate_collection(self, collection_name, vector_size):
        delete_ops = StorageOps(delete_collection=collection_name)
        try:
            self.collection_api.update_collections(storage_ops=delete_ops)
        except Exception as e:
            print("Exception when calling CollectionsApi->update_collections: %s\n" % e)
        create_ops = StorageOps(create_collection=StorageOpsAnyOfCreateCollection(
            distance=Distance(value="Cosine"),
            name=collection_name,
            vector_size=vector_size,
        ))
        try:
            self.collection_api.update_collections(storage_ops=create_ops)
        except qdrant_openapi_client.ApiException as e:
            print("Exception when calling CollectionsApi->update_collections: %s\n" % e)

    def upload_point(self, collection_name: str, points: List[PointStruct]):
        self.point_api.update_points(
            collection_name,
            collection_update_operations=CollectionUpdateOperations(
                upsert_points=PointInsertOps(points=points)
            ))

    @classmethod
    def data_to_payload_request(cls, obj: dict) -> Dict[str, PayloadInterface]:
        """
        >>> QdrantClient.data_to_payload_request({"idx": 123})['idx'].to_dict()
        {'type': 'integer', 'value': 123}
        """
        res = {}
        for key, val in obj.items():
            if isinstance(val, int):
                res[key] = PayloadInterface(value=val, type="integer", _check_type=False)
            if isinstance(val, float):
                res[key] = PayloadInterface(value=val, type="float", _check_type=False)
            if isinstance(val, str):
                res[key] = PayloadInterface(value=val, type="keyword", _check_type=False)

        return res

    @classmethod
    def make_point(cls, idx, vector, payload):
        return PointStruct(
            id=idx,
            vector=vector,
            payload=cls.data_to_payload_request(payload)
        )

