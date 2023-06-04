.PHONY: 

migration-up:
	alembic upgrade head

migration-down:
	alembic downgrade base

migration-init:
	alembic init migrations

middleware-up:
	docker compose -f docker-compose-debug.yml -f docker-compose-middleware.yml up -d

middleware-down: 
	docker compose -f docker-compose-debug.yml -f docker-compose-middleware.yml down

OMTB_app-run:
	cd OMTB_app && uvicorn main:app --host 0.0.0.0 --port 8888

docker-up:
	docker compose -f docker-compose-debug.yml up -d