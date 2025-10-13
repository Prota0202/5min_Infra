cat > /tmp/run.sh <<'SH'
#!/bin/sh
set -eu

NAMESPACE="${NAMESPACE:-test}"
DEPLOYMENT="${DEPLOYMENT:-projet2025}"

echo "🔁 Rollout restart du déploiement $DEPLOYMENT dans $NAMESPACE"
kubectl -n "$NAMESPACE" rollout restart "deployment/$DEPLOYMENT"

echo "⏳ Attente de la fin du rollout…"
kubectl -n "$NAMESPACE" rollout status "deployment/$DEPLOYMENT" --timeout=5m

echo "✅ Terminé."
SH
