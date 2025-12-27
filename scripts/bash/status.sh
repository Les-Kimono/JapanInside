#!/bin/bash

echo "========================================================"
echo "   JapanInside - Statut"
echo "========================================================"
echo ""

NAMESPACE=$(kubectl get namespace japaninside -o jsonpath='{.metadata.name}' 2>/dev/null)
if [ -z "$NAMESPACE" ]; then
    echo "X Application non deployee"
    echo "  Lancer: ./scripts/bash/deploy.sh"
    exit 1
fi

echo "Pods:"
kubectl get pods -n japaninside

echo ""
echo "Services:"
kubectl get svc -n japaninside

# Verifier les IPs LoadBalancer
BACKEND_IP=$(kubectl get svc backend -n japaninside -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null)
FRONTEND_IP=$(kubectl get svc frontend -n japaninside -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null)

echo ""
echo "URLs d'acces:"
if [ -n "$FRONTEND_IP" ]; then
    echo "  Frontend: http://${FRONTEND_IP}:5173"
else
    echo "  Frontend: <en attente - tunnel non lance?>"
fi
if [ -n "$BACKEND_IP" ]; then
    echo "  Backend:  http://${BACKEND_IP}:8000"
else
    echo "  Backend:  <en attente - tunnel non lance?>"
fi

echo ""

