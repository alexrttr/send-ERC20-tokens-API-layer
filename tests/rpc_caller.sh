#!/bin/sh

curl -sS -d '{"id":"json","method":"sendTokens","params":["0x56e00846302d048dbaa81a3748916c0d906491b2", "0.01", "1234"] }' http://localhost:7080  | tee out.html
