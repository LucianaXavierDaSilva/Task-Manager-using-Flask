import pytest
import requests
import os

# Obtém a BASE_URL da variável de ambiente, com um valor padrão para local
BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:5000/")

# Ajuste para Docker: substitui o valor padrão se estiver rodando no Docker
# No ambiente do GitLab CI, a variável de ambiente BASE_URL será definida no .gitlab-ci.yml
# Portanto, a lógica abaixo pode não ser estritamente necessária, mas pode ser mantida
# como um fallback ou para testes locais em Docker.
if os.environ.get("DOCKER_ENV") == "true":
    BASE_URL = os.environ.get("BASE_URL", "http://192.168.98.10:8080/")
    print(f"BASE_URL dentro do container (DOCKER_ENV=true): {BASE_URL}") # Para debug

print(f"BASE_URL sendo usada para os testes: {BASE_URL}") # Para debug

def test_create_task_with_empty_title():
    task_data = {"title": "", "description": "This task has no title"}
    response = requests.post(f"{BASE_URL}/tasks", json=task_data)
    assert response.status_code == 400

def test_update_task():
    task_data = {"title": "Original Title", "description": "Original description"}
    create_response = requests.post(f"{BASE_URL}/tasks", json=task_data)
    assert create_response.status_code == 201 # Assumindo que a criação retorna 201 Created
    task_id = create_response.json().get("id")
    assert task_id is not None, "Task ID não encontrado na resposta de criação"
    updated_data = {"title": "Updated Title", "description": "Updated description"}
    response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json().get("title") == "Updated Title"





