#!/bin/sh

curl -sS -d '{"id":"json","method":"addAddressToWhitelist","params":["0x55532b5187a9cb711f3e215a442e65b82525a2db", "1234abc"] }' http://localhost:7080  | tee  -a out.html

curl -sS -d '{"id":"json","method":"addAddressToWhitelist","params":["0x21e66e44BCCD87c3f3a598bc1f14e2353D0ace72", "4321cba"] }' http://localhost:7080  | tee  -a out.html
