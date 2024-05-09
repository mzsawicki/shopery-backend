lint:
	docker compose run api poetry run mypy --config-file mypy.init .
migrate:
	docker compose run api poetry run alembic upgrade head
build:
	docker compose up --build -d --remove-orphans
up:
	docker compose up -d
down:
	docker compose down --remove-orphans
log:
	docker compose logs
ps:
	docker compose ps
test:
	docker compose -f docker-compose.test.yml build tests && docker compose -f docker-compose.test.yml run tests poetry run pytest
bootstrap:
	docker compose run api poetry run python -m src.bootstrap
