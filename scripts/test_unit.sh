#!/bin/sh
echo "Executando testes unitários..."
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install pytest pytest-cov
pytest --cov=todo_project --cov-report=xml:coverage.xml tests/unitary
