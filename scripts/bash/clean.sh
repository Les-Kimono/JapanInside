#!/bin/bash

# Supprime les ressources Kubernetes JapanInside
# Usage: 
#   ./scripts/bash/clean.sh            # Demande confirmation
#   ./scripts/bash/clean.sh --force    # Supprime sans confirmation
#   ./scripts/bash/clean.sh --all      # Supprime tout + Minikube

set -e

FORCE=false
ALL=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --force|-f)
            FORCE=true
            shift
            ;;
        --all|-a)
            ALL=true
            shift
            ;;
        *)
            echo "Usage: $0 [--force] [--all]"
            echo "  --force : Supprime sans confirmation"
            echo "  --all   : Supprime tout + Minikube"
            exit 1
            ;;
    esac
done

echo "========================================================="
echo "   JapanInside - Nettoyage Kubernetes"
echo "========================================================="
echo ""

if [ "$ALL" = true ]; then
    echo "[WARNING] Mode --all : Suppression complete (Minikube inclus)"
else
    echo "Suppression des ressources JapanInside uniquement"
fi

# Demander confirmation si --force n'est pas specifie
if [ "$FORCE" = false ]; then
    read -p "Continuer? (o/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Oo]$ ]]; then
        echo "Operation annulee."
        exit 0
    fi
fi

echo ""
echo "[CLEAN] Suppression des ressources Kubernetes..."
kubectl delete -f k8s/frontend/ --ignore-not-found
kubectl delete -f k8s/backend/ --ignore-not-found
kubectl delete -f k8s/db/ --ignore-not-found
kubectl delete -f k8s/config/ --ignore-not-found

if [ "$ALL" = true ]; then
    echo ""
    echo "[CLEAN] Arret et suppression de Minikube..."
    minikube stop
    minikube delete
fi

echo ""
echo "[SUCCESS] Nettoyage termine!"
echo ""
