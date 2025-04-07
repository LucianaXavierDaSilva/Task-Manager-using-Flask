FROM python:3.11.2-slim-buster
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
COPY todo_project/ /app/todo_project/
ENV SECRET_KEY=45cf93c4d41348cd9980674ade9a7356
VOLUME /app/todo_project/instance
EXPOSE 5000
CMD ["python", "/app/todo_project/run.py"]

