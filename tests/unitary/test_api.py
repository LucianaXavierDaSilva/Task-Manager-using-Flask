import pytest
from datetime import datetime
from todo_project.todo_project import app, db, bcrypt
from todo_project.todo_project.models import Task, User

@pytest.fixture
def test_client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_create_task_model():
    with app.app_context():
        # Cria usuário de teste
        user = User.query.filter_by(username='luciana').first()
        if not user:
            hashed_password = bcrypt.generate_password_hash("rnpesr").decode("utf-8")
            user = User(username='luciana', email='luciana@example.com', password=hashed_password)
            db.session.add(user)
            db.session.commit()

        # Cria task associada ao usuário
        new_task = Task(
            title='Unit Test Task',
            description='This is a unit test for the model',
            due_date=datetime.utcnow(),
            completed=False,
            user_id=user.id
        )
        db.session.add(new_task)
        db.session.commit()

        retrieved_task = Task.query.filter_by(title='Unit Test Task').first()
        assert retrieved_task is not None
        assert retrieved_task.description == 'This is a unit test for the model'
        assert retrieved_task.user_id == user.id

def test_task_model_completion():
    with app.app_context():
        # Cria usuário de teste
        user = User.query.filter_by(username='luciana').first()
        if not user:
            hashed_password = bcrypt.generate_password_hash("rnpesr").decode("utf-8")
            user = User(username='luciana', email='luciana@example.com', password=hashed_password)
            db.session.add(user)
            db.session.commit()

        # Cria task associada ao usuário
        task = Task(
            title='Model Completion Test',
            description='Testing task completion in model',
            completed=False,
            user_id=user.id
        )
        db.session.add(task)
        db.session.commit()

        task.completed = True
        db.session.commit()

        completed_task = Task.query.filter_by(title='Model Completion Test').first()
        assert completed_task.completed is True

def test_route_home_unit(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Task Manager" in response.data  # Conteúdo esperado na página inicial

def test_route_add_task_unit(test_client):
    response = test_client.get('/add')  # Supondo que a rota de adicionar tarefas seja '/add'
    assert response.status_code == 200
    assert b"Add New Task" in response.data  # Conteúdo esperado na página de adicionar tarefa
