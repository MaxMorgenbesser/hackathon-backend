FROM python:3.12.3

WORKDIR /app
COPY . /app

RUN pip3 install -r requirements.txt


EXPOSE 8080


CMD uvicorn main:app --host 0.0.0.0 --port 8080 --reload
