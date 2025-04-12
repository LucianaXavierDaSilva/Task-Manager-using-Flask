import pytest
from datetime import datetime
from todo_project import create_app, db, bcrypt
from todo_project.models import Task, User

# ========== FIXTURES ==========

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def create_test_user(app):
    def _create_user(username='luciana', password='rnpesr'):
        with app.app_context():
            user = User.query.filter_by(username=username).first()
            if not user:
                hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
                user = User(username=username, password=hashed_pw)
                db.session.add(user)
                db.session.commit()
            return user
    return _create_user

@pytest.fixture
def logged_in_client(app, client, create_test_user):
    create_test_user()  # Garantir que o usuário existe
    response = client.post('/login', data={
        'username': 'luciana',
        'password': 'rnpesr'
    }, follow_redirects=True)
    assert b'Task Manager' in response.data or b'All Tasks' in response.data
    return client

# ========== TESTES DE MODELO ==========

def test_create_task_model(app, create_test_user):
    with app.app_context():
        user = create_test_user()
        user_id = user.id  # Captura antes de sair do contexto da sessão

        task = Task(
            title='Unit Test Task',
            description='This is a unit test for the model',
            due_date=datetime.utcnow(),
            completed=False,
            user_id=user_id
        )
        db.session.add(task)
        db.session.commit()

        retrieved_task = Task.query.filter_by(title='Unit Test Task').first()
        assert retrieved_task is not None
        assert retrieved_task.description == 'This is a unit test for the model'
        assert retrieved_task.user_id == user_id
        assert not retrieved_task.completed

def test_task_model_completion(app, create_test_user):
    with app.app_context():
        user = create_test_user()
        user_id = user.id  # Captura antes de sair do contexto da sessão

        task = Task(
            title='Model Completion Test',
            description='Testing task completion in model',
            completed=False,
            user_id=user_id
        )
        db.session.add(task)
        db.session.commit()

        task.completed = True
        db.session.commit()

        completed_task = Task.query.get(task.id)
        assert completed_task.completed is True

# ========== TESTES DE ROTAS ==========

def test_route_home_unit(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Task Manager" in response.data or b"About" in response.data

def test_route_add_task_unit(logged_in_client):
    response = logged_in_client.get('/add_task')
    assert response.status_code == 200
    assert b"Add Task" in response.data or b"Task Description" in response.data
