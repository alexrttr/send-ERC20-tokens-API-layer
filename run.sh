#!/bin/bash

docker-compose -f geth_light_node.yaml up&  # -d
docker-compose up --scale worker=2 --no-deps &  # -d
