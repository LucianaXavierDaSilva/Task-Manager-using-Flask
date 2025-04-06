

import pytest
import requests
import os

# Obtém a BASE_URL da variável de ambiente, com um valor padrão para local
BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:5000/")

# Ajuste para Docker: substitui o valor padrão se estiver rodando no Docker
if os.environ.get("DOCKER_ENV") == "true":
    BASE_URL = "http://192.168.98.10:8080/"

def test_create_task_with_empty_title():
    task_data = {"title": "", "description": "This task has no title"}
    response = requests.post(f"{BASE_URL}/tasks", json=task_data)
    assert response.status_code == 400

def test_update_task():
    task_data = {"title": "Original Title", "description": "Original description"}
    create_response = requests.post(f"{BASE_URL}/tasks", json=task_data)
    task_id = create_response.json()["id"]
    updated_data = {"title": "Updated Title", "description": "Updated description"}
    response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"




