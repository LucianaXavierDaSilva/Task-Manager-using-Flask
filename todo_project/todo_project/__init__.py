from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
import os
from dotenv import load_dotenv
import logging

# Carrega variáveis do .env
load_dotenv()

# Configuração básica de logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Inicializa extensões (sem app ainda)
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Configurações da aplicação
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'site.db')

    # Garante que o diretório 'instance' exista
    os.makedirs(app.instance_path, exist_ok=True)

    # Valida se SECRET_KEY está definida
    if not app.config['SECRET_KEY']:
        raise ValueError("A variável de ambiente SECRET_KEY não está definida.")

    # Inicializa extensões com o app
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    # Importa rotas e modelos no contexto da aplicação
    from . import routes, models

    return app
