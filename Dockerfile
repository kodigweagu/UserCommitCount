FROM python:3.8
COPY ./app /app

RUN pip install fastapi uvicorn requests redis pytest-docker-compose

EXPOSE 8080

CMD ["uvicorn", "--app-dir", "/app", "main:app", "--host", "0.0.0.0", "--port", "8080" ]