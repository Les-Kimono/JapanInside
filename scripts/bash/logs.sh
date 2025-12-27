#!/bin/bash

SERVICE="${1:-backend}"

echo "========================================================"
echo "   JapanInside - Logs"
echo "========================================================"
echo ""

if [ "$SERVICE" = "all" ]; then
    echo "Affichage des logs de tous les services..."
    echo "Appuyer sur Ctrl+C pour arreter"
    echo ""
    kubectl logs -n japaninside -l app --tail=50 -f
elif [ "$SERVICE" = "frontend" ]; then
    echo "Logs Frontend (Ctrl+C pour arreter)..."
    echo ""
    kubectl logs -n japaninside -l app=frontend --tail=100 -f
else
    echo "Logs Backend (Ctrl+C pour arreter)..."
    echo ""
    kubectl logs -n japaninside -l app=backend --tail=100 -f
fi

