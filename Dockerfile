FROM python:3-alpine

WORKDIR /app

RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY flask-app .

EXPOSE 8000

CMD ["python", "app.py"]
