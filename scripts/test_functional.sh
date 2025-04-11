#!/bin/sh
echo "Executando testes funcionais..."
docker-compose up -d
apk add --no-cache python3 py3-pip curl
pip3 install -r requirements.txt pytest requests
echo "Aguardando app subir..."
sleep 10
pytest tests/functional
docker-compose down

