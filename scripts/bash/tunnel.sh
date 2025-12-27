#!/bin/bash

echo "========================================================"
echo "   Minikube Tunnel - LoadBalancer"
echo "========================================================"
echo ""

# Verifier Minikube
STATUS=$(minikube status --format='{{.Host}}' 2>/dev/null)
if [ "$STATUS" != "Running" ]; then
    echo "X Minikube n'est pas demarre!"
    echo "  Demarrer avec: minikube start"
    exit 1
fi

echo "OK Minikube est demarre"
echo ""
echo "IMPORTANT:"
echo "  - Ce terminal doit rester OUVERT"
echo "  - Appuyer sur Ctrl+C pour arreter le tunnel"
echo "  - Necessite les privileges sudo"
echo ""
echo "Demarrage du tunnel..."
echo "========================================================"
echo ""

# Demarrer le tunnel (necessite sudo)
minikube tunnel

