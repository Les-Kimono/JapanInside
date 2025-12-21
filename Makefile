
SERVICES := frontend backend db

first-install:
	docker-compose build

start:
	docker-compose up -d

stop:
	docker-compose down

purge:
	docker-compose down -v

restart: stop start
build: docker-compose -f docker-compose.prod.yml up --build -d