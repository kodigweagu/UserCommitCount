FROM python:3.8
RUN pip install fastapi uvicorn
COPY ./app /app
CMD ["uvicorn", "app.main:app", "--host", "localhost", "--port", "8080" ]