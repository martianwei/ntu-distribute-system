.PHONY: migration-up migration-down migration-init run-middleware build-middleware

migration-up:
	alembic upgrade head

migration-down:
	alembic downgrade base

migration-init:
	alembic init migrations

run-middleware:
	docker compose -f dokerk-compose-middleware up -d

build-middleware:
	docker compose -f dokerk-compose-middleware build

run-OMTB_app:
	uvicorn OMTB_app.main:app --host 0.0.0.0 --port 8888