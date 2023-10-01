#!/bin/bash
set -Eeuo pipefail

cd "$(dirname "$0")"

git pull

ENV_DIR="backend/env"
if [ ! -d $ENV_DIR ]
then
	python3 -m venv backend/env
fi

source backend/env/bin/activate
apt-get install libjpeg-dev zlib1g-dev -y
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade pillow
python3 -m pip install -r backend/requirements.txt

npm ci --dev
frontend/node_modules/.bin/parcel build frontend/bundles-src/index.js --dist-dir backend/bundles --public-url="./"

python3 backend/manage.py collectstatic --noinput
python3 backend/manage.py migrate --noinput

systemctl daemon-reload
systemctl restart star-burger
systemctl reload nginx

./backend/rollbar_status.sh

echo "deploy success"
