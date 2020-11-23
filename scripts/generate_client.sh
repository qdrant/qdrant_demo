#!/usr/bin/env bash
# This script will generate Qdant client from OpenAPI definitions


docker run --rm \
    -u $(id -u ${USER}):$(id -g ${USER}) \
    -v "${PWD}:/local" openapitools/openapi-generator-cli generate \
    -i https://raw.githubusercontent.com/qdrant/qdrant/master/openapi/openapi.yaml \
    -g python \
    -o /local/qdrant_client