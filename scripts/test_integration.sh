#!/bin/sh
echo "Executando testes de integração..."
docker-compose up -d
apk add --no-cache python3 py3-pip curl
pip3 install -r requirements.txt pytest requests beautifulsoup4 lxml
echo "Aguardando app subir..."
sleep 10
pytest tests/integration
docker-compose down
