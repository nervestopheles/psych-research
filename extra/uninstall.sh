#!/bin/env bash
set -e
source env.sh

docker stop $NAME > /dev/null
docker rm $NAME > /dev/null
docker volume rm $VOLUME > /dev/null

echo "Uninstall complete"
