#!/bin/sh

curl -sS -d '{"id":"json","method":"sendTokens","params":["0x949f409DfEB9a97cf5a6105533B7A666791A8D0a", "0.01", "1234"] }' http://localhost:7080  | tee out.html
