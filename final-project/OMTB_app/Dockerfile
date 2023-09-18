FROM python:3.9-slim-buster

WORKDIR /app

ADD . .

RUN apt-get update -y && \
    pip3 install -r requirements.txt

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8888"]

