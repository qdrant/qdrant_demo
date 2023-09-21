#!/usr/bin/env bash


rsync -avP --exclude='venv' \
           --exclude='__pycache__' \
           --exclude='frontend' \
           --exclude='frontend_v2' \
           --exclude='.idea' \
           . $1:./project/qdrant_demo/


