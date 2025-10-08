#!/usr/bin/env bash
set -euo pipefail

# Ajouter le repo ingress-nginx si besoin
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx >/dev/null 2>&1 || true
helm repo update

# Créer le namespace si pas présent
kubectl get ns ingress-nginx >/dev/null 2>&1 || kubectl create namespace ingress-nginx

# Installer ou mettre à jour l'ingress-nginx
helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --set controller.watchIngressWithoutClass=true \
  --set controller.publishService.enabled=true

echo "✅ ingress-nginx installé/mis à jour dans le namespace 'ingress-nginx'."
kubectl -n ingress-nginx get svc ingress-nginx-controller
