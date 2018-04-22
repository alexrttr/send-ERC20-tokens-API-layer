#!/bin/sh

curl -sS -d '{"id":"json","method":"addAddressToWhitelist","params":["0x55532B5187a9cB711f3E215A442e65b82525a2Db", "1234abc"] }' http://localhost:7080  | tee  -a out.html

curl -sS -d '{"id":"json","method":"addAddressToWhitelist","params":["0x21e66e44BCCD87c3f3a598bc1f14e2353D0ace72", "4321cba"] }' http://localhost:7080  | tee  -a out.html
