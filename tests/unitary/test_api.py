import pytest
from todo_project.todo_project import app, db
from todo_project.models import Task  # Importe seus modelos
from datetime import datetime

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
        new_task = Task(title='Unit Test Task', description='This is a unit test for the model', due_date=datetime.utcnow())
        db.session.add(new_task)
        db.session.commit()
        retrieved_task = Task.query.filter_by(title='Unit Test Task').first()
        assert retrieved_task is not None
        assert retrieved_task.description == 'This is a unit test for the model'

def test_task_model_completion():
    with app.app_context():
        task = Task(title='Model Completion Test', description='Testing task completion in model', completed=False)
        db.session.add(task)
        db.session.commit()
        task.completed = True
        db.session.commit()
        completed_task = Task.query.filter_by(title='Model Completion Test').first()
        assert completed_task.completed is True

def test_route_home_unit(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Task Manager" in response.data # Verifique se algum conteúdo esperado está na resposta

def test_route_add_task_unit(test_client):
    response = test_client.get('/add') # Assumindo que você tem uma rota para adicionar tarefas
    assert response.status_code == 200
    assert b"Add New Task" in response.data # Verifique se algum conteúdo esperado está na resposta

