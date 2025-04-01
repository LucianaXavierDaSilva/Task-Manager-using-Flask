FROM python:3.11.2-slim-buster
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
COPY todo_project/ /app/todo_project/
EXPOSE 5000
CMD ["python", "/app/todo_project/run.py"]

