#!/bin/sh

echo "=== Executando testes unitários ==="

# Falha o script em qualquer erro
set -e

# Cria e ativa ambiente virtual
python -m venv venv
. venv/bin/activate

# Instala dependências
pip install --upgrade pip
pip install -r requirements.txt
pip install pytest pytest-cov

# Define PYTHONPATH explicitamente para o pacote Flask
export PYTHONPATH="$PYTHONPATH:$(pwd)/todo_project"

# Executa testes unitários com relatório de cobertura
pytest --cov=todo_project tests/unitary/ --cov-report=xml
