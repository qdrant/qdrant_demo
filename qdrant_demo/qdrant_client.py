import os
from typing import Dict

import openapi_client
from openapi_client.api.collections_api import CollectionsApi
from openapi_client.api.points_api import PointsApi
from openapi_client.model.distance import Distance
from openapi_client.model.payload_interface import PayloadInterface
from openapi_client.model.payload_variant_for_int64 import PayloadVariantForInt64
from openapi_client.model.point_struct import PointStruct
from openapi_client.model.storage_ops import StorageOps
from openapi_client.model.storage_ops_any_of_create_collection import StorageOpsAnyOfCreateCollection


QDRANT_HOST = os.environ.get("QDRANT_HOST", "localhost")
QDRANT_PORT = os.environ.get("QDRANT_PORT", 6333)


class QdrantClient:

    @classmethod
    def _get_qdrant_client(cls):
        configuration = openapi_client.Configuration(
            host=f"http://{QDRANT_HOST}:{QDRANT_PORT}"
        )
        api_client = openapi_client.ApiClient(configuration)
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
        except openapi_client.ApiException as e:
            print("Exception when calling CollectionsApi->update_collections: %s\n" % e)

    @classmethod
    def data_to_payload_request(cls, obj: dict) -> Dict[str, PayloadInterface]:
        """
        >>> QdrantClient.data_to_payload_request({"idx": 123})['idx'].to_dict()
        {"value": 123, "type": "integer"}
        """
        res = {}
        for key, val in obj.items():
            if isinstance(val, int):
                res[key] = PayloadInterface(value=val, type="integer")
            if isinstance(val, float):
                res[key] = PayloadInterface(value=val, type="float")
            if isinstance(val, str):
                res[key] = PayloadInterface(value=val, type="keyword")

        return res

    def make_point(self, idx, vector, payload):
        PointStruct(
            id=idx,
            vector=vector,
            payload=self.data_to_payload_request(payload)
        )

if __name__ == '__main__':
    PayloadInterface.validations