lint:
	docker-compose run api poetry run mypy --config-file mypy.init .
migrate:
	docker-compose run api poetry run alembic upgrade head
build:
	docker-compose up --build -d --remove-orphans
up:
	docker-compose up -d
down:
	docker-compose down --remove-orphans
log:
	docker-compose logs
test:
	docker-compose -f docker-compose.test.yml run tests poetry run pytest
bootstrap-local:
	awslocal s3api create-bucket --bucket product-images
	awslocal s3api create-bucket --bucket brand-logos