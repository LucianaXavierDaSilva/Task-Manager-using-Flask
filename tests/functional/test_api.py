import pytest
import requests
import os

# Obtém a BASE_URL da variável de ambiente
BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:5000/")
print(f"BASE_URL sendo usada para os testes funcionais: {BASE_URL}")

def get_csrf_token_functional():
    """Obtém o token CSRF da página inicial (ou de alguma página protegida) para testes da API."""
    response = requests.get(f"{BASE_URL}/add_task") # Uma página protegida que requer login
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    csrf_token = soup.find('input', {'name': 'csrf_token'})
    if csrf_token and 'value' in csrf_token.attrs:
        return csrf_token['value']
    else:
        raise Exception("Campo 'csrf_token' não encontrado na página para testes funcionais.")

def test_create_task_with_empty_title():
    csrf_token = get_csrf_token_functional()
    task_data = {"title": "", "description": "This task has no title", "csrf_token": csrf_token}
    response = requests.post(f"{BASE_URL}/tasks", data=task_data) # Use 'data' para form-urlencoded
    assert response.status_code == 400

def test_update_task():
    csrf_token = get_csrf_token_functional()
    # Primeiro, crie uma tarefa (isso pode ser simplificado se houver um endpoint de listagem)
    create_data = {"title": "Original Title", "description": "Original description", "csrf_token": csrf_token}
    create_response = requests.post(f"{BASE_URL}/tasks", data=create_data)
    assert create_response.status_code == 201
    task_id = create_response.json().get("id")
    assert task_id is not None

    updated_data = {"title": "Updated Title", "description": "Updated description", "csrf_token": csrf_token}
    response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=updated_data) # Assumindo que PUT é usado para update
    assert response.status_code == 200
    assert response.json().get("title") == "Updated Title"

# Adicione mais testes funcionais conforme necessário



