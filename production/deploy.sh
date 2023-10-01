#!/bin/bash

cd "$(dirname "$0")"

set -Eeuo pipefail

docker-compose up -d frontend
docker-compose up -d backend
../rollbar_status.sh

echo "Production deploy success"
