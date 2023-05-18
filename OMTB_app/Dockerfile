FROM python:3.9-slim-buster

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
WORKDIR /app
ADD ./OMTB_app .

RUN apt-get update -y 

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8888"]
