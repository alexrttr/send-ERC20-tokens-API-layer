#!/bin/bash

if ! [ -f ethereum/keys/ethereum/password ]
then
  echo "Password file is not found, please find README.txt and make sure you have both keystore and password in place"
  exit -1
fi

docker-compose up -d --scale worker=2 
