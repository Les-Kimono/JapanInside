#!/bin/bash
# Deploiement de JapanInside sur Kubernetes avec Load Balancer
# Usage: ./scripts/bash/deploy.sh

echo "========================================================"
echo "   Deploiement JapanInside"
echo "========================================================"
echo ""

# Verifier kubectl
if ! command -v kubectl &> /dev/null; then
    echo "X kubectl non trouve"
    echo "  Installer kubectl"
    exit 1
fi

# Verifier Minikube
MINIKUBE_STATUS=$(minikube status --format='{{.Host}}' 2>/dev/null)
if [ "$MINIKUBE_STATUS" != "Running" ]; then
    echo "Minikube non demarre. Demarrage..."
    minikube start
    if [ $? -ne 0 ]; then
        echo "X Echec du demarrage de Minikube"
        exit 1
    fi
fi

echo "[1/4] Deploiement du namespace..."
kubectl apply -f k8s/config/

echo ""
echo "[2/4] Deploiement de la base de donnees..."
kubectl apply -f k8s/db/

echo "  Attente de PostgreSQL..."
kubectl wait --namespace=japaninside --for=condition=ready pod -l app=postgres --timeout=180s

echo ""
echo "[3/4] Deploiement du backend - 3 replicas..."
kubectl apply -f k8s/backend/

echo ""
echo "[4/4] Deploiement du frontend - 3 replicas..."
kubectl apply -f k8s/frontend/

echo ""
echo "  Attente que les pods soient prets..."
kubectl wait --namespace=japaninside --for=condition=ready pod -l app=backend --timeout=120s
kubectl wait --namespace=japaninside --for=condition=ready pod -l app=frontend --timeout=120s

echo ""
echo "OK Deploiement termine!"
echo ""
kubectl get pods -n japaninside

echo ""
echo "========================================================"
echo "   Etape Suivante"
echo "========================================================"
echo ""
echo "Ouvrir un NOUVEAU terminal et lancer:"
echo "  ./scripts/bash/tunnel.sh"
echo ""
echo "Puis verifier le statut avec:"
echo "  ./scripts/bash/status.sh"
echo ""

