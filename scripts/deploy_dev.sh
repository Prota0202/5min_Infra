#!/usr/bin/env bash
set -euo pipefail

# Namespace dev
kubectl apply -f k8s/namespace-dev.yaml

# Déployer/mettre à jour l'app
kubectl -n dev apply -f k8s/deployment.yaml
kubectl -n dev apply -f k8s/service.yaml
kubectl -n dev apply -f k8s/ingress.yaml

echo "⏳ Attente que les pods soient prêts..."
kubectl -n dev rollout status deploy/projet2025

echo "✅ Déployé. Ingress:"
kubectl -n dev get ingress projet2025 -o wide
