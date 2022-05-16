#!/bin/env bash
set -e
source env.sh

docker volume create $VOLUME > /dev/null
echo "Create volume: '$VOLUME'"

docker run -d \
    --net host \
    --name $NAME \
    -e POSTGRES_PASSWORD=$DBPASS \
    -e POSTGRES_DB=$DB \
    -e PGDATA=/var/lib/postgresql/data/pgdata \
    -v $VOLUME:/var/lib/postgresql/data \
    postgres:14.2 > /dev/null
echo "Create container: '$NAME'" && echo

docker ps
