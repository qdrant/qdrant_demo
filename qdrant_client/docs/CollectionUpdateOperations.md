# CollectionUpdateOperations

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**upsert_points** | [**PointInsertOps**](PointInsertOps.md) |  | defaults to nulltype.Null
**delete_points** | [**PointOpsAnyOf1DeletePoints**](PointOpsAnyOf1DeletePoints.md) |  | defaults to nulltype.Null
**set_payload** | [**PayloadOpsAnyOfSetPayload**](PayloadOpsAnyOfSetPayload.md) |  | defaults to nulltype.Null
**delete_payload** | [**PayloadOpsAnyOf1DeletePayload**](PayloadOpsAnyOf1DeletePayload.md) |  | defaults to nulltype.Null
**clear_payload** | [**PayloadOpsAnyOf2ClearPayload**](PayloadOpsAnyOf2ClearPayload.md) |  | defaults to nulltype.Null
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


