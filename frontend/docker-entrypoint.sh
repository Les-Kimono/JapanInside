#!/bin/sh
set -e

# Définir l'URL du backend par défaut si non définie
BACKEND_URL=${BACKEND_URL:-http://backend:8000}

echo "🔧 Configuration Nginx avec BACKEND_URL=$BACKEND_URL"

# Remplacer ${BACKEND_URL} dans la config Nginx
envsubst '${BACKEND_URL}' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf

echo "✅ Configuration Nginx prête !"
cat /etc/nginx/conf.d/default.conf

# Démarrer Nginx
exec nginx -g 'daemon off;'

