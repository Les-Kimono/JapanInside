
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


# Deploiement avec Load Balancer
deploy:
	@bash scripts/bash/deploy.sh

# Statut de l'application
status:
	@bash scripts/bash/status.sh

# Tunnel LoadBalancer (doit rester ouvert)
tunnel:
	@bash scripts/bash/tunnel.sh

# Logs
logs-backend:
	@bash scripts/bash/logs.sh backend

logs-frontend:
	@bash scripts/bash/logs.sh frontend

logs-all:
	@bash scripts/bash/logs.sh all

# Nettoyage
clean:
	@bash scripts/bash/clean.sh

# Redeploy
redeploy: clean deploy

# Endpoints et scaling
endpoints:
	@echo "📊 Service Endpoints:"
	@kubectl get endpoints -n japaninside

scale-up:
	@echo "📈 Scaling up to 5 replicas..."
	@kubectl scale deployment backend -n japaninside --replicas=5
	@kubectl scale deployment frontend -n japaninside --replicas=5
	@echo "✅ Scaled up!"
	@kubectl get pods -n japaninside

scale-down:
	@echo "📉 Scaling down to 2 replicas..."
	@kubectl scale deployment backend -n japaninside --replicas=2
	@kubectl scale deployment frontend -n japaninside --replicas=2
	@echo "✅ Scaled down!"
	@kubectl get pods -n japaninside

# Aide
help:
	@echo "📚 Commandes Disponibles:"
	@echo ""
	@echo "Deploiement:"
	@echo "  make deploy        - Deploie l'application avec Load Balancer (3 replicas)"
	@echo "  make tunnel        - Lance le tunnel Minikube (requis pour LoadBalancer)"
	@echo "  make status        - Affiche l'etat et les URLs"
	@echo "  make clean         - Supprime tous les deploiements"
	@echo "  make redeploy      - Nettoie et redemarre"
	@echo ""
	@echo "Logs:"
	@echo "  make logs-backend  - Affiche les logs du backend"
	@echo "  make logs-frontend - Affiche les logs du frontend"
	@echo "  make logs-all      - Affiche tous les logs"
	@echo ""
	@echo "Load Balancer:"
	@echo "  make endpoints     - Affiche les endpoints (distribution)"
	@echo "  make scale-up      - Scale a 5 replicas"
	@echo "  make scale-down    - Scale a 2 replicas"
	@echo ""
	@echo "Docker:"
	@echo "  make first-install - Build les images Docker"
	@echo "  make start         - Demarre les containers"
	@echo "  make stop          - Arrete les containers"
	@echo "  make restart       - Redemarre les containers"