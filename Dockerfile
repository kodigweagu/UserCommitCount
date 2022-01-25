FROM python:3.8
COPY ./app /app
COPY ./requirements.txt /app

RUN pip install -r requirements.txt
RUN pip install fastapi uvicorn

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--reload" ]