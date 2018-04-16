#!/bin/sh

curl -sS -d '{"id":"json","method":"sendTokens","params":["0x56E00846302d048dbAa81a3748916c0d906491b2", "5", "1234"] }' http://localhost:7080  | tee out.html
