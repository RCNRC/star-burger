#!/bin/bash
set -Eeuo pipefail

cd "$(dirname "$0")"

export $( grep -vE "^(#.*|\s*)$" backend/.env )

END_TIME="$(date)"

REVISION="$(git rev-parse HEAD)"
COMMENT="$(git log --format=%B -n 1 $REVISION)"
DIRECTORY="$(pwd)"
LOCAL_USER="$(whoami)"

if [ ! -z ${ROLLBAR_ACCESS_TOKEN+x} ];
then curl -H "X-Rollbar-Access-Token: $ROLLBAR_ACCESS_TOKEN" -H "Content-Type: application/json" -X POST 'https://api.rollbar.com/api/1/deploy' -d "{\"environment\": \"production\", \"revision\": \"$REVISION\", \"rollbar_name\": \"unknown\", \"local_username\": \"$LOCAL_USER\", \"comment\": \"$COMMENT\", \"status\": \"succeeded\", \"code_version\": \"$REVISION\", \"server\": {\"root\": \"file://$DIRECTORY/\"}}";
fi

echo "Rollbar status success"
