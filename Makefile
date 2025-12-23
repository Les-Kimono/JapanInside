
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

# ========================================
# Kubernetes / Minikube Deployment
# ========================================

deploy:
	@echo "🚀 Deploying to Kubernetes..."
	kubectl apply -f k8s/config/
	kubectl apply -f k8s/db/
	@echo "⏳ Waiting for PostgreSQL to be ready..."
	kubectl wait --namespace=japaninside --for=condition=ready pod -l app=postgres --timeout=180s
	kubectl apply -f k8s/backend/
	kubectl apply -f k8s/frontend/
	@echo "⏳ Waiting for all pods to be ready..."
	kubectl wait --namespace=japaninside --for=condition=ready pod -l app=backend --timeout=120s
	kubectl wait --namespace=japaninside --for=condition=ready pod -l app=frontend --timeout=120s
	@echo "✅ Deployment complete!"
	@echo ""
	kubectl get pods -n japaninside
	@echo ""
	kubectl get svc -n japaninside

k8s-status:
	@echo "📊 Kubernetes Status:"
	kubectl get pods -n japaninside
	kubectl get svc -n japaninside
	kubectl get pvc -n japaninside

k8s-logs-backend:
	kubectl logs -n japaninside -l app=backend --tail=100 -f

k8s-logs-frontend:
	kubectl logs -n japaninside -l app=frontend --tail=100 -f

k8s-logs-db:
	kubectl logs -n japaninside -l app=postgres --tail=100 -f

k8s-access-frontend:
	@echo "🌐 Opening frontend service..."
	minikube service frontend -n japaninside

k8s-access-backend:
	@echo "🌐 Opening backend service..."
	minikube service backend -n japaninside

k8s-clean:
	@echo "🧹 Cleaning Kubernetes resources..."
	kubectl delete -f k8s/frontend/ --ignore-not-found
	kubectl delete -f k8s/backend/ --ignore-not-found
	kubectl delete -f k8s/db/ --ignore-not-found
	kubectl delete -f k8s/config/ --ignore-not-found
	@echo "✅ Cleanup complete!"

k8s-restart: k8s-clean k8s-deploy

k8s-help:
	@echo "📚 Kubernetes Commands:"
	@echo "  make k8s-deploy          - Deploy application to Kubernetes"
	@echo "  make k8s-status          - Show deployment status"
	@echo "  make k8s-logs-backend    - Show backend logs"
	@echo "  make k8s-logs-frontend   - Show frontend logs"
	@echo "  make k8s-logs-db         - Show database logs"
	@echo "  make k8s-access-frontend - Open frontend in browser"
	@echo "  make k8s-access-backend  - Open backend in browser"
	@echo "  make k8s-clean           - Remove all deployments"
	@echo "  make k8s-restart         - Clean and redeploy"