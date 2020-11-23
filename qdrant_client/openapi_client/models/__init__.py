# coding: utf-8

# flake8: noqa

# import all models into this package
# if you have many models here with many references from one model to another this may
# raise a RecursionError
# to avoid this, import only the models that you directly need like:
# from from openapi_client.model.pet import Pet
# or import this package, but before doing it, use:
# import sys
# sys.setrecursionlimit(n)

from openapi_client.model.collection_description import CollectionDescription
from openapi_client.model.collection_info import CollectionInfo
from openapi_client.model.collection_update_operations import CollectionUpdateOperations
from openapi_client.model.collections_response import CollectionsResponse
from openapi_client.model.condition import Condition
from openapi_client.model.condition_any_of import ConditionAnyOf
from openapi_client.model.condition_any_of1 import ConditionAnyOf1
from openapi_client.model.condition_any_of2 import ConditionAnyOf2
from openapi_client.model.condition_any_of3 import ConditionAnyOf3
from openapi_client.model.condition_any_of4 import ConditionAnyOf4
from openapi_client.model.distance import Distance
from openapi_client.model.error_response import ErrorResponse
from openapi_client.model.error_response_status import ErrorResponseStatus
from openapi_client.model.filter import Filter
from openapi_client.model.indexes import Indexes
from openapi_client.model.indexes_any_of import IndexesAnyOf
from openapi_client.model.indexes_any_of1 import IndexesAnyOf1
from openapi_client.model.indexes_any_of1_options import IndexesAnyOf1Options
from openapi_client.model.inline_response200 import InlineResponse200
from openapi_client.model.inline_response2001 import InlineResponse2001
from openapi_client.model.inline_response2002 import InlineResponse2002
from openapi_client.model.inline_response2003 import InlineResponse2003
from openapi_client.model.inline_response2004 import InlineResponse2004
from openapi_client.model.inline_response2005 import InlineResponse2005
from openapi_client.model.inline_response2006 import InlineResponse2006
from openapi_client.model.payload_ops import PayloadOps
from openapi_client.model.payload_ops_any_of import PayloadOpsAnyOf
from openapi_client.model.payload_ops_any_of1 import PayloadOpsAnyOf1
from openapi_client.model.payload_ops_any_of1_delete_payload import PayloadOpsAnyOf1DeletePayload
from openapi_client.model.payload_ops_any_of2 import PayloadOpsAnyOf2
from openapi_client.model.payload_ops_any_of2_clear_payload import PayloadOpsAnyOf2ClearPayload
from openapi_client.model.payload_ops_any_of_set_payload import PayloadOpsAnyOfSetPayload
from openapi_client.model.payload_type import PayloadType
from openapi_client.model.payload_type_any_of import PayloadTypeAnyOf
from openapi_client.model.payload_type_any_of1 import PayloadTypeAnyOf1
from openapi_client.model.payload_type_any_of2 import PayloadTypeAnyOf2
from openapi_client.model.payload_type_any_of3 import PayloadTypeAnyOf3
from openapi_client.model.point_ops import PointOps
from openapi_client.model.point_ops_any_of import PointOpsAnyOf
from openapi_client.model.point_ops_any_of1 import PointOpsAnyOf1
from openapi_client.model.point_ops_any_of1_delete_points import PointOpsAnyOf1DeletePoints
from openapi_client.model.point_request import PointRequest
from openapi_client.model.record import Record
from openapi_client.model.scored_point import ScoredPoint
from openapi_client.model.search_params import SearchParams
from openapi_client.model.search_params_any_of import SearchParamsAnyOf
from openapi_client.model.search_params_any_of_hnsw import SearchParamsAnyOfHnsw
from openapi_client.model.search_request import SearchRequest
from openapi_client.model.segment_config import SegmentConfig
from openapi_client.model.storage_ops import StorageOps
from openapi_client.model.storage_ops_any_of import StorageOpsAnyOf
from openapi_client.model.storage_ops_any_of1 import StorageOpsAnyOf1
from openapi_client.model.storage_ops_any_of2 import StorageOpsAnyOf2
from openapi_client.model.storage_ops_any_of2_change_aliases import StorageOpsAnyOf2ChangeAliases
from openapi_client.model.storage_ops_any_of_create_collection import StorageOpsAnyOfCreateCollection
from openapi_client.model.storage_type import StorageType
from openapi_client.model.storage_type_any_of import StorageTypeAnyOf
from openapi_client.model.storage_type_any_of1 import StorageTypeAnyOf1
from openapi_client.model.update_result import UpdateResult
from openapi_client.model.update_status import UpdateStatus
