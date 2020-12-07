#!/usr/bin/env bash

npm run build

rsync -avP ./dist/ $1:./project/web-deployment/public/demo/

