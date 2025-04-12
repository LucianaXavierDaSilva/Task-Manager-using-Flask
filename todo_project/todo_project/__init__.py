from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate  # 👈 Importa o Migrate
from flask_wtf.csrf import CSRFProtect
import os
from dotenv import load_dotenv
import logging

load_dotenv()  # Carrega variáveis do .env

# Configuração básica de logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'site.db')

# Inicializa extensões
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # 👈 Adiciona suporte a flask db migrate/upgrade
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Garante que o diretório 'instance' exista
os.makedirs(app.instance_path, exist_ok=True)

from . import models
from . import routes

# Valida se SECRET_KEY está configurada
if not app.config['SECRET_KEY']:
    raise ValueError("A variável de ambiente SECRET_KEY não está definida.")
