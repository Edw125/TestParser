#!/bin/bash

set -e
host="db"
port="3306"
cmd="./docker-entrypoint.sh"

until curl http://"$host":"$port" --http0.9; do
  sleep 5
done

exec $cmd
