#!/bin/sh
echo "Compilando imagem Docker..."
docker build -t task-manager-estudo-caso:latest .
echo "Imagem Docker construída com sucesso."
