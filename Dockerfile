FROM python:3.11.2-slim-buster
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
COPY todo_project/ /app/todo_project/
COPY create_db.py /app/create_db.py
RUN python /app/create_db.py
VOLUME /app/todo_project/todo_project/site.db # Declara um volume para o arquivo de banco de dados
EXPOSE 5000
CMD ["python", "/app/todo_project/run.py"]


