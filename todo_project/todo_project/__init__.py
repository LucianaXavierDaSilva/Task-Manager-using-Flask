from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv
import logging
from flask_wtf.csrf import CSRFProtect  # Importe CSRFProtect

load_dotenv()  # Carrega as variáveis de ambiente do .env

# Configuração básica de logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)  # Inicialize a proteção CSRF

from . import models
from . import routes

if not app.config['SECRET_KEY']:
    raise ValueError("A variável de ambiente SECRET_KEY não está definida.")

