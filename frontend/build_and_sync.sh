#!/usr/bin/env bash

pnpm run build

rsync -avP ./dist/ $1:./project/web-deployment/public/demo/

