#!/bin/sh

echo "=== Executando testes unitários ==="

# Cria e ativa ambiente virtual
python -m venv venv
. venv/bin/activate

# Instala dependências
pip install --upgrade pip
pip install -r requirements.txt
pip install pytest pytest-cov

# Adiciona diretório atual ao PYTHONPATH para evitar erro de importação
export PYTHONPATH=$(pwd)

# Executa testes unitários com cobertura
pytest tests/unitary --cov=todo_project --cov-report=xml
