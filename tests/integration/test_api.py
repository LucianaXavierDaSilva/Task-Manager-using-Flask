import pytest
import requests
import os
from bs4 import BeautifulSoup
import time  # Adicionado para lidar com possíveis atrasos na inicialização do container

# Obtém a BASE_URL da variável de ambiente, com um valor padrão para local
BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:5000/")

# Ajuste para Docker: usa a variável de ambiente definida no .gitlab-ci.yml
# A verificação DOCKER_ENV não é mais estritamente necessária aqui, pois confiamos na BASE_URL
print(f"BASE_URL sendo usada para os testes de integração: {BASE_URL}")

# Usar uma sessão global para persistir os cookies entre as requisições
session = requests.Session()
csrf_token_global = None

@pytest.fixture(scope="session", autouse=True)
def authenticate_session():
    global csrf_token_global
    login_url = f"{BASE_URL}/login"
    max_retries = 5
    retry_delay = 2  # segundos

    for attempt in range(max_retries):
        try:
            login_page_response = session.get(login_url)
            login_page_response.raise_for_status()
            soup = BeautifulSoup(login_page_response.text, 'lxml')
            csrf_token = soup.find('input', {'name': 'csrf_token'})
            if csrf_token and 'value' in csrf_token.attrs:
                csrf_token_value = csrf_token['value']
                login_data = {"username": "luciana", "password": "rnpesr", "csrf_token": csrf_token_value}
                login_response = session.post(login_url, data=login_data)
                login_response.raise_for_status()
                csrf_token_global = get_task_csrf_token() # Obter o token para as tarefas após o login
                print(f"Token CSRF para tarefas obtido (autenticação): {csrf_token_global}")
                print(f"Cookies de login (autenticação): {session.cookies}")
                return  # Autenticação bem-sucedida
            else:
                print(f"Tentativa {attempt + 1}: Campo 'csrf_token' não encontrado ou sem valor. Retentando em {retry_delay} segundos...")
        except requests.exceptions.RequestException as e:
            print(f"Tentativa {attempt + 1}: Erro ao acessar a página de login: {e}. Retentando em {retry_delay} segundos...")
        time.sleep(retry_delay)

    raise Exception("Falha na autenticação da sessão de testes após várias tentativas.")

def get_task_csrf_token():
    protected_page_response = session.get(f"{BASE_URL}/add_task")
    protected_page_response.raise_for_status()
    soup = BeautifulSoup(protected_page_response.text, 'lxml')
    csrf_token_tasks = soup.find('input', {'name': 'csrf_token'})
    if csrf_token_tasks and 'value' in csrf_token_tasks.attrs:
        return csrf_token_tasks['value']
    else:
        raise Exception("Erro: Campo 'csrf_token' não encontrado na página de adicionar tarefa.")

def test_create_task():
    global csrf_token_global
    task_data = {"task_name": "Test Task", "csrf_token": csrf_token_global} # Use 'task_name' para corresponder ao formulário
    response = session.post(f"{BASE_URL}/add_task", data=task_data, follow_redirects=True) # Simula envio do formulário
    print(f"\nStatus code da requisição (criar tarefa): {response.status_code}")
    print(f"Conteúdo da resposta (criar tarefa):\n{response.text[:500]}")
    assert response.status_code == 200
    assert b"Test Task" in response.data

def test_get_task():
    global csrf_token_global
    # Primeiro, crie uma tarefa para poder buscá-la
    task_data = {"task_name": "Test Task to Get", "csrf_token": csrf_token_global}
    create_response = session.post(f"{BASE_URL}/add_task", data=task_data, follow_redirects=True)
    assert create_response.status_code == 200
    assert b"Test Task to Get" in create_response.data

    # Extrai o ID da tarefa da página (isso é uma simplificação, em uma API real você usaria JSON)
    soup = BeautifulSoup(create_response.text, 'lxml')
    task_link = soup.find('a', string='Test Task to Get') # Adapte o seletor conforme sua template
    if task_link and 'href' in task_link.attrs:
        task_id_match = task_link['href'].split('/')[-2] # Supondo um padrão /all_tasks/<id>/...
        try:
            task_id = int(task_id_match)
            response = session.get(f"{BASE_URL}/all_tasks/{task_id}/update_task") # Rota de visualização/edição
            assert response.status_code == 200
            assert b"Test Task to Get" in response.data
        except ValueError:
            pytest.fail("Não foi possível extrair o ID da tarefa para o teste de get.")
    else:
        pytest.fail("Não foi possível encontrar o link da tarefa para o teste de get.")

# Adicione mais testes de integração conforme necessário


