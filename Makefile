.PHONY: up down

up:
	alembic upgrade head

down:
	alembic downgrade base

install:
	pip install -r requirements.txt

init:
	alembic init alembic