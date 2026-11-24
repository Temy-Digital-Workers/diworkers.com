#!/bin/sh
# Ship the marketplace service to the hub droplet and (re)start it.
set -e
HOST=root@161.35.25.14; KEY=~/.ssh/id_ed25519; DST=/opt/diworkers/marketplace
cd "$(dirname "$0")"
scp -i $KEY app.py requirements.txt Dockerfile compose.yml $HOST:$DST/
ssh -i $KEY $HOST "cd $DST && docker compose up -d --build live test emulator && sleep 4 && curl -fsS http://127.0.0.1:8710/marketplace/healthz && echo && curl -fsS http://127.0.0.1:8711/marketplace/healthz"
