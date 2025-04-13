import logging
from todo_project import create_app

# Configura o logging para salvar em /logs/flask.log
logging.basicConfig(
    filename='/logs/flask.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
