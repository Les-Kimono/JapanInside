#!/bin/bash

echo "========================================================"
echo "   JapanInside - Nettoyage"
echo "========================================================"
echo ""

echo "Ceci va supprimer toutes les ressources JapanInside"
read -p "Continuer? (o/N): " CONFIRM

if [ "$CONFIRM" != "o" ] && [ "$CONFIRM" != "O" ]; then
    echo "Annule."
    exit 0
fi

echo ""
echo "Nettoyage en cours..."
kubectl delete -f k8s/frontend/ --ignore-not-found
kubectl delete -f k8s/backend/ --ignore-not-found
kubectl delete -f k8s/db/ --ignore-not-found
kubectl delete -f k8s/config/ --ignore-not-found

echo ""
echo "OK Nettoyage termine!"
echo ""

