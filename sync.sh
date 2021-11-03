#!/usr/bin/env bash


rsync -avP --exclude='venv' \
           --exclude='__pycache__' \
           --exclude='frontend' \
           --exclude='.idea' \
           --exclude='data' \
           . $1:./project/qdrant_demo_websummit/


