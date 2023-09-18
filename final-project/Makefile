.PHONY: 

migration-up:
	alembic upgrade head

migration-down:
	alembic downgrade base

migration-init:
	alembic init migrations

service-up:
	docker compose -f docker-compose-debug.yml -f docker-compose-middleware.yml up -d

service-down: 
	docker compose -f docker-compose-debug.yml -f docker-compose-middleware.yml down