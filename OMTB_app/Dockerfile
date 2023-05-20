FROM python:3.9-slim-buster

WORKDIR /app

ADD . .

RUN apt-get update -y 

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8888"]

