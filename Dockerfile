FROM python:3.8

WORKDIR /app

COPY ./app /app
COPY requirements.txt /app

RUN pip install pip --upgrade && pip install -r /app/requirements.txt

EXPOSE 8080

CMD ["uvicorn", "--app-dir", "/app", "main:app", "--host", "0.0.0.0", "--port", "8080" ]