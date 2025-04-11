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
export PYTHONPATH="$PYTHONPATH:$(pwd)/todo_project"

# Executa testes unitários com cobertura
pytest --cov=todo_project tests/unitary/ --cov-report=xml
