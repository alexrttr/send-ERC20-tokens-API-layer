#!/bin/sh

curl -sS -d '{"id":"json","method":"addAddressToWhitelist","params":["0x55532B5187a9cB711f3E215A442e65b82525a2Db", "1234"] }' http://localhost:7080  | tee out.html
