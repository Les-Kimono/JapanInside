
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


all-purge:
	@echo "Stopping all running containers..."
	@containers=$$(docker ps -aq); if [ -n "$$containers" ]; then docker stop $$containers; fi
	@echo "Removing all containers..."
	@containers=$$(docker ps -aq); if [ -n "$$containers" ]; then docker rm -f $$containers; fi
	@echo "Removing all images..."
	@images=$$(docker images -aq); if [ -n "$$images" ]; then docker rmi -f $$images; fi
	@echo "Removing all volumes..."
	@volumes=$$(docker volume ls -q); if [ -n "$$volumes" ]; then docker volume rm $$volumes; fi
	@echo "Removing all networks..."
	@networks=$$(docker network ls -q); if [ -n "$$networks" ]; then docker network rm $$networks; fi
	@echo "All Docker resources have been purged."
pre-commit:
	pre-commit run --all-files --config .github/pre-commit.yml

tests:
	pytest backend/tests -v