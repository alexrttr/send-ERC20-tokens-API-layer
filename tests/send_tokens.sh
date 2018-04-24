#!/bin/sh

curl -sS -d '{"id":"json","method":"sendTokens","params":["0x56E00846302d048dbAa81a3748916c0d906491b2", "5", "1234"] }' http://localhost:7080  | tee out.html
curl -sS -d '{"id":"json","method":"sendTokens","params":["0x21e66e44bccd87c3f3a598bc1f14e2353d0ace72", "10", "1234"] }' http://localhost:7080  | tee out.html

