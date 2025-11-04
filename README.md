### 1. Onboarding Guide for New Developers

Ce guide explique comment configurer l'environnement de développement local à l'aide de `docker-compose.yml` pour lancer les services `web` et `mongodb`.

1.  Clonez le dépôt : `git clone https://github.com/Prota0202/5min_Infra.git`
2.  Lancez les services : `docker-compose up --build`

### 2. CI/CD Pipeline Details

Le pipeline CI/CD (`.github/workflows/ci-test.yml`) automatise les tests et la publication des images Docker de l'application sur Docker Hub.

### 3. Database Setup

- **MongoDB** : L'application utilise MongoDB en mode **Replica Set** en production, déployé via un `StatefulSet` (`mongodb-statefulset.yaml`) pour la résilience. Un déploiement plus simple (`mongodb-deployment.yaml`) est utilisé pour l'environnement de test.
- **Redis** : Un `StatefulSet` est également utilisé pour le déploiement de Redis en production (`redis.yaml`), assurant la persistance et la stabilité du cache.
- **Migration** : Le script `update_dates.py` permet une migration manuelle des données.

###### 1. Copier le script à l'intérieur du pod de l'application

        kubectl cp update_dates.py prod/projet2025-5778b954d9-psnvm:/app/update_dates.py

###### 2. Ouvrir un terminal interactif dans le pod

        kubectl exec -it projet2025-5778b954d9-psnvm -n prod -- bash

###### 3. Exécuter le script avec Python

        python update_dates.py

### 4. Monitoring & Scaling

- **Monitoring** : Kubernetes gère la santé de l'application via des `readinessProbe` et `livenessProbe` configurées dans les fichiers de déploiement.
- **Scaling** : Le nombre de répliques est défini dans les fichiers de déploiement (ex: `replicas: 3`), permettant à Kubernetes de répartir la charge.

---

### 5. Cluster Setup Instructions

**5.1. Déploiement de l'environnement de Test/Dev**

Cet environnement est défini par les fichiers dans `k8s/test/`. L'ordre de déploiement est le suivant :

1.  **Créez le Namespace** :

    - Le namespace `dev` doit être créé en premier pour isoler l'environnement.

    ```bash
    kubectl apply -f k8s/test/namespace-dev.yaml
    ```

2.  **Déployez l'application de test** :

    - Déploie l'application, son service et son point d'accès externe (Ingress).

    ```bash
    kubectl apply -f k8s/test/deployment.yaml
    kubectl apply -f k8s/test/service.yaml
    kubectl apply -f k8s/test/ingress.yaml
    ```

    - **Note** : Les pods de l'application peuvent entrer en `CrashLoopBackOff` tant que la base de données n'est pas disponible.

3.  **Déployez la base de données MongoDB** :
    - Déploie une instance MongoDB simple pour l'environnement de test. Une fois ce service disponible, les pods de l'application devraient redémarrer et se connecter correctement.
    ```bash
    kubectl apply -f k8s/test/mongodb-deployment.yaml
    kubectl apply -f k8s/test/mongodb-service.yaml
    ```
    - Afin de créer la schématique de la DB dans le pod principale il fautt utiliser la même strategie que la migration.C'est-à-dire créer un script, le copier dans un pod et l'excecuter comme expliquer ci-dessus.

**5.2. Déploiement de l'environnement de Production**

Cet environnement utilise les fichiers de configuration situés à la racine du projet.

1.  **Déployez le Namespace** :

    ```bash
    kubectl apply -f k8s/prod/namespace-prod.yaml
    ```

2.  **Déployez MongoDB en Replica Set** :

    - Le `StatefulSet` assure un déploiement robuste.

    ```bash
    kubectl apply -f mongodb-svc.yaml # Service pour le statefulset
    kubectl apply -f mongodb-statefulset.yaml
    ```

3.  **Déployez Redis** :

    ```bash
    kubectl apply -f redis-prod.yaml # Service pour Redis
    kubectl apply -f redis.yaml # StatefulSet Redis
    ```

4.  **Déployez l'Application de Production** :
    ```bash
    kubectl apply -f deployment-prod.yaml
    kubectl apply -f service-prod.yaml
    kubectl apply -f ingressProd.yaml
    ```
