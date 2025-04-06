import sys
import os
from dotenv import load_dotenv

load_dotenv()

# Adiciona ao sys.path o diretório que contém o seu pacote de aplicação ('todo_project' interno)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.join(BASE_DIR, "todo_project")
sys.path.append(APP_DIR)

print("sys.path:", sys.path)

from todo_project import app, db

with app.app_context():
    db.create_all()
    print("Banco de dados criado!")







