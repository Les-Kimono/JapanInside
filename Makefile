
SERVICES := frontend backend db
MINIKUBE_ENV := $(shell minikube docker-env --shell bash)
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


# --------------------------------------------------
# Kubernetes
# --------------------------------------------------

# Build des images dans Minikube pour prendre en compte les changements
k8s-build:
	@echo "Configurer Docker pour Minikube..."
	eval $(minikube docker-env)
	docker build -t japaninside-backend -f ./backend/Dockerfile.prod ./backend
	docker build -t japaninside-frontend -f ./frontend/Dockerfile.prod ./frontend

# Appliquer les manifests K8s
k8s-apply:
	@echo "Appliquer tous les manifests K8s..."
	kubectl apply -f k8s/db/
	kubectl apply -f k8s/backend/
	kubectl apply -f k8s/frontend/

# Supprimer tous les pods/services K8s
k8s-delete:
	@echo "Supprimer tous les pods/services K8s..."
	kubectl delete -f k8s/frontend/ --ignore-not-found
	kubectl delete -f k8s/backend/ --ignore-not-found
	kubectl delete -f k8s/db/ --ignore-not-found

# Redéployer proprement
k8s-restart: k8s-delete k8s-apply

# Logs
k8s-logs-db:
	kubectl logs -f statefulset/postgres

# Port forwarding
k8s-frontend-start:
	kubectl port-forward svc/frontend 5173:5173

k8s-backend-start:
	kubectl port-forward svc/backend 8000:8000

# --------------------------------------------------
# Commande unique pour rebuild + redeployer tous les services K8s
# --------------------------------------------------
k8s-up: k8s-build k8s-apply
	@echo "Toutes les images rebuildées et manifests appliqués. Les pods vont se mettre à jour..."