import pytest
from datetime import datetime
from todo_project.todo_project import app, db, bcrypt
from todo_project.todo_project.models import Task, User

# ====== FIXTURES ======

@pytest.fixture
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Banco em memória
    app.config['WTF_CSRF_ENABLED'] = False  # Desativa CSRF para testes

    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()


@pytest.fixture
def logged_in_client(test_client):
    with app.app_context():
        # Garante que o usuário existe
        user = User.query.filter_by(username='luciana').first()
        if not user:
            hashed_pw = bcrypt.generate_password_hash('rnpesr').decode('utf-8')
            user = User(username='luciana', password=hashed_pw)
            db.session.add(user)
            db.session.commit()

    # Faz login via POST na rota /login
    response = test_client.post('/login', data={
        'username': 'luciana',
        'password': 'rnpesr'
    }, follow_redirects=True)
    assert b'Task Manager' in response.data or b'All Tasks' in response.data
    return test_client

# ====== TESTES DE MODEL ======

def test_create_task_model():
    with app.app_context():
        user = User.query.filter_by(username='luciana').first()
        if not user:
            hashed_password = bcrypt.generate_password_hash("rnpesr").decode("utf-8")
            user = User(username='luciana', password=hashed_password)
            db.session.add(user)
            db.session.commit()

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
        user = User.query.filter_by(username='luciana').first()
        if not user:
            hashed_password = bcrypt.generate_password_hash("rnpesr").decode("utf-8")
            user = User(username='luciana', password=hashed_password)
            db.session.add(user)
            db.session.commit()

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

# ====== TESTES DE ROTAS ======

def test_route_home_unit(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Task Manager" in response.data or b"About" in response.data

def test_route_add_task_unit(logged_in_client):
    response = logged_in_client.get('/add_task')
    assert response.status_code == 200
    assert b"Add Task" in response.data or b"Task Description" in response.data
