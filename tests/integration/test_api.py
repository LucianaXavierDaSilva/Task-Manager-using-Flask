import pytest
import requests
import os
from bs4 import BeautifulSoup

# Obtém a BASE_URL da variável de ambiente, com um valor padrão para local
BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:5000/")

# Ajuste para Docker: substitui o valor padrão se estiver rodando no Docker
if os.environ.get("DOCKER_ENV") == "true":
    BASE_URL = "http://192.168.98.10:8080/"

# Usar uma sessão global para persistir os cookies entre as requisições
session = requests.Session()
csrf_token_global = None

@pytest.fixture(scope="session", autouse=True)
def authenticate_session():
    global csrf_token_global
    login_url = f"{BASE_URL}/login"
    login_page_response = session.get(login_url)
    print(f"\nStatus code da página de login (autenticação): {login_page_response.status_code}")
    print(f"URL da página de login (autenticação): {login_page_response.url}")
    print(f"Conteúdo da página de login (primeiros 500 chars) (autenticação):\n{login_page_response.text[:500]}")
    login_page_response.raise_for_status()
    soup = BeautifulSoup(login_page_response.text, 'lxml')
    csrf_token = soup.find('input', {'name': 'csrf_token'})
    if csrf_token:
        csrf_token_value = csrf_token['value']
        print(f"Token CSRF para login obtido (autenticação): {csrf_token_value}")
        login_data = {"username": "luciana", "password": "rnpesr", "csrf_token": csrf_token_value}
        login_response = session.post(login_url, data=login_data)
        login_response.raise_for_status()
        csrf_token_global = get_task_csrf_token() # Obter o token para as tarefas após o login
        print(f"Token CSRF para tarefas obtido (autenticação): {csrf_token_global}")
        print(f"Cookies de login (autenticação): {session.cookies}")
    else:
        print("Erro: Campo 'csrf_token' não encontrado no formulário de login (autenticação).")
        raise Exception("Falha na autenticação da sessão de testes.")

def get_task_csrf_token():
    protected_page_response = session.get(f"{BASE_URL}/add_task")
    protected_page_response.raise_for_status()
    soup = BeautifulSoup(protected_page_response.text, 'lxml')
    csrf_token_tasks = soup.find('input', {'name': 'csrf_token'})['value']
    return csrf_token_tasks

def test_create_task():
    global csrf_token_global
    task_data = {"title": "Test Task", "description": "This is a test task", "csrf_token": csrf_token_global}
    response = session.post(f"{BASE_URL}/tasks", data=task_data) # Use 'data' aqui
    print(f"\nHeaders da requisição (criar tarefa): {response.request.headers}")
    print(f"Conteúdo da resposta (criar tarefa): {response.text}")
    assert response.status_code == 201
    assert response.json()["title"] == "Test Task"

def test_get_task():
    global csrf_token_global
    task_data = {"title": "Test Task to Get", "description": "This task will be retrieved", "csrf_token": csrf_token_global}
    create_response = session.post(f"{BASE_URL}/tasks", data=task_data, cookies=session.cookies) # Use 'data' aqui
    print(f"\nHeaders da requisição (criar tarefa para get): {create_response.request.headers}")
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]
    response = session.get(f"{BASE_URL}/tasks/{task_id}", cookies=session.cookies)
    print(f"Headers da requisição (get tarefa): {response.request.headers}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task to Get"

# Adicione mais testes de integração conforme necessário

