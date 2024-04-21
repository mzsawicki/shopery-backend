build:
	docker-compose up --build -d --remove-orphans
up:
	docker-compose up -d
down:
	docker-compose down
log:
	docker-compose logs