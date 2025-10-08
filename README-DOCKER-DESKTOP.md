# Docker Desktop + Kubernetes — Guide de déploiement

Ce guide déploie votre application Flask répliquée derrière **ingress-nginx** dans Kubernetes intégré à Docker Desktop (pas de Minikube).

## Prérequis
- Docker Desktop avec **Kubernetes activé** (Settings → Kubernetes → Enable Kubernetes)
- `kubectl` et `helm` installés

## 1) Installer l'Ingress Controller (ingress-nginx)
```bash
./scripts/install_ingress_nginx.sh
kubectl -n ingress-nginx get pods
```

## 2) Construire l'image localement
```bash
docker build -t projet2025:v1 .
```

## 3) Déployer en namespace `dev`
```bash
./scripts/deploy_dev.sh
kubectl -n dev get all
kubectl -n dev get ingress projet2025
```

## 4) Accéder à l'application
- Essayez : http://projet.localtest.me
  - `localtest.me` pointe toujours vers 127.0.0.1 (utile pour tester l'Ingress en local).
- Si vous préférez `localhost`, faites un port-forward (optionnel) :
  ```bash
  kubectl -n ingress-nginx port-forward svc/ingress-nginx-controller 8080:80
  ```
  Puis ouvrez : http://localhost:8080

## 5) Mettre à jour (rollout zéro downtime)
- Rebuild une nouvelle image avec un nouveau tag (ex. `v2`) :
  ```bash
  docker build -t projet2025:v2 .
  ```
- Éditez `k8s/deployment.yaml` pour mettre `image: projet2025:v2`, puis :
  ```bash
  kubectl -n dev apply -f k8s/deployment.yaml
  kubectl -n dev rollout status deploy/projet2025
  ```

## Fichiers ajoutés
- `scripts/install_ingress_nginx.sh` : installe l'Ingress Controller.
- `scripts/deploy_dev.sh` : crée le namespace, applique les manifests.
- `k8s/namespace-dev.yaml` : namespace `dev`.
- `k8s/ingress.yaml` : règle Ingress pour l'hôte `projet.localtest.me`.
```
