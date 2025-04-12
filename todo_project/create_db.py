from todo_project import create_app, db
from todo_project.models import User, Task  # Certifica-se de que as tabelas sejam criadas

# Cria a aplicação Flask com base nas configurações padrão
app = create_app()

# Cria todas as tabelas no contexto da aplicação
with app.app_context():
    db.create_all()
    print("Banco de dados criado com sucesso!")



