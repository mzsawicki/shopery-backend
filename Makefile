lint:
	docker-compose run api poetry run mypy --config-file mypy.init .
migrate:
	docker-compose run api poetry run alembic upgrade head
build:
	docker-compose up --build -d --remove-orphans
up:
	docker-compose up -d
down:
	docker-compose down
log:
	docker-compose logs