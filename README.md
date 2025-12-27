# JapanInside

## Table des matières
- [Badges](#badges)
- [Équipe](#équipe)
- [Descriptif](#descriptif)
- [Idée](#idée)
- [Stack technique](#stack-technique)
- [Structure du projet](#structure-du-projet)
- [Setup](#setup)
- [Pipeline CI](#pipeline-ci)
- [Makefiles](#makefiles)
- [Pipeline CD](#pipeline-cd)
- [Déploiement avec Minikube](#déploiement-avec-minikube)

---

## Badges

[![CI Frontend](https://github.com/Les-Kimono/JapanInside/actions/workflows/ci-frontend.yml/badge.svg)](https://github.com/ORG/Les-Kimono/JapanInside/workflows/ci-frontend.yml)  
[![CI Backend](https://github.com/Les-Kimono/JapanInside/actions/workflows/ci-backend.yml/badge.svg)](https://github.com/ORG/Les-Kimono/JapanInside/workflows/ci-backend.yml)

![Status](https://img.shields.io/badge/status-en%20développement-orange?style=for-the-badge)  
![Licence](https://img.shields.io/github/license/Les-Kimono/JapanInside?style=for-the-badge)  
![Dernier commit](https://img.shields.io/github/last-commit/Les-Kimono/JapanInside?style=for-the-badge)  
![Contributeurs](https://img.shields.io/github/contributors/Les-Kimono/JapanInside?style=for-the-badge)  
![Équipe](https://img.shields.io/badge/team-Les--Kimono-blue?style=for-the-badge)  

---

## Équipe

- [@justine](https://github.com/WitheredFlower10)  
- [@lucas](https://github.com/luucas7)  
- [@adrien](https://github.com/baffionia)  
- [@jordan](https://github.com/ZedRoff)  
- [@auguste](https://github.com/ZedRoff)  
- [@aman](https://github.com/ZedRoff)  

---

## Descriptif

Ce projet a été réalisé dans le cadre de l'unité DevOps, encadrée par M. Badr TAJINI, en 2ème année d'ingénieur à l'école ESIEE Paris (E4FI).

L’objectif est d’appliquer les pratiques DevOps sur un projet existant : pipelines CI/CD, dockerisation, Kubernetes (Minikube) et gestion du travail collaboratif sur GitHub.

---

## Idée

JapanInside est une application full-stack pour organiser un voyage au Japon.  

- **Front-office** : visualisation des étapes du voyage, attractions et spécialités culinaires.  
- **Back-office** : gestion et édition du voyage, ajout d’étapes, attractions et recettes.

---

## Stack technique

| Côté | Technologie |
|------|------------|
| Front-End | ReactJS |
| Back-End | FastAPI |
| Base de données | PostgreSQL |
| Conteneurisation | Docker |
| Orchestration | Kubernetes (Minikube) |
| Load Balancing | Service LoadBalancer (3 replicas) |
| Registry | Docker Hub |

---

## Structure du projet

```
.
├── backend
│   ├── crud
│   ├── data
│   ├── models
│   ├── routes
│   ├── schemas
│   ├── tests
│   └── utils
├── frontend
│   ├── public
│   └── src
├── k8s
│   ├── backend
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   ├── config
│   │   └── namespace.yaml
│   ├── db
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   └── frontend
│       ├── deployment.yaml
│       └── service.yaml
└── scripts
    ├── bash/              # Scripts bash (Linux/Mac)
    │   ├── deploy.sh
    │   ├── tunnel.sh
    │   ├── status.sh
    │   ├── logs.sh
    │   └── clean.sh
    ├── deploy.ps1         # Scripts PowerShell (Windows)
    ├── tunnel.ps1
    ├── status.ps1
    ├── logs.ps1
    └── clean.ps1
```

Le projet inclut des **tests unitaires** pour le front et le back, des **Makefiles**, des **pre-commit hooks**, des **scripts de déploiement PowerShell**, et un code prêt pour la production avec **load balancing**.

---

## Setup

### Installation

Cloner le projet :  

**HTTPS :**
```bash
git clone https://github.com/Les-Kimono/JapanInside.git japan-inside
```

**SSH :**
```bash
git clone git@github.com:Les-Kimono/JapanInside.git japan-inside
```

Puis accéder au dossier :
```bash
cd japan-inside
```

---

### Lancement du projet

```bash
make first-install
make start
make stop
make start
```

> Les deux dernières étapes sont nécessaires pour que la base de données se crée correctement.

---

### Développement local

```bash
git checkout staging
make restart
```

---
## Images Docker

```
https://hub.docker.com/r/luucas71/japaninside-frontend
https://hub.docker.com/r/luucas71/japaninside-backend
```
## Pipeline CI

Deux pipelines distincts sont utilisés pour le front-end et le back-end.

### Front-end

- Setup
- Linting
- Security Check
- Build
- Unit Testing

### Back-end

- Setup
- Code Sniffing
- Linting
- Safety Check
- Unit Testing

---

## Makefiles

Trois Makefiles sont présents :

1. **Racine** : lancer Kubernetes, tests unitaires front et back, build Docker.  
2. **Backend** : tests unitaires, linting, code sniffing, container back.  
3. **Frontend** : tests unitaires, linting, code sniffing, container front.  

---

## Pipeline CD

Le pipeline de déploiement continu (CD) automatise le processus de mise en production de l'application sur Kubernetes.

### Workflow de déploiement

Lors d'un push sur la branche `main`, le pipeline s'exécute automatiquement :

#### 1. Build des images Docker

Deux images de production sont construites à partir des Dockerfiles optimisés :

- **Backend** : `Dockerfile.prod` avec FastAPI + Uvicorn
- **Frontend** : `Dockerfile.prod` avec build optimisé Vite

Les images sont taguées avec :
- `latest` pour la version la plus récente
- Le hash du commit Git pour traçabilité

#### 2. Push sur Docker Hub

Les images sont poussées sur Docker Hub dans le repository public :

```
luucas71/japaninside-backend:latest
luucas71/japaninside-frontend:latest
```

#### 3. Déploiement sur Kubernetes (Minikube)

Les images sont automatiquement déployées sur un cluster Kubernetes local (Minikube) qui simule un environnement de production.

**Architecture déployée :**

```
┌─────────────────────────────────┐
│   LoadBalancer Service          │
│   (Distribution automatique)    │
└───────────┬─────────────────────┘
            │
    ┌───────┼────────┐
    │       │        │
┌───▼──┐ ┌──▼──┐ ┌──▼──┐
│Pod 1 │ │Pod 2│ │Pod 3│
└──────┘ └─────┘ └─────┘
```

**Composants déployés :**

- **PostgreSQL** : Base de données avec PersistentVolumeClaim
- **Backend** : 3 replicas avec LoadBalancer
- **Frontend** : 3 replicas avec LoadBalancer

**Avantages du load balancing :**

- Répartition automatique du trafic entre les pods (round-robin)
- Haute disponibilité : si un pod tombe, le trafic est redirigé vers les autres
- Scalabilité : possibilité d'ajuster le nombre de replicas selon la charge
- Auto-healing : redémarrage automatique des pods défaillants

---

## Déploiement avec Minikube

### Linux / Mac

#### Prérequis

- **Minikube**
- **kubectl**
- **make**

#### Démarrage rapide avec Makefile

Le Makefile simplifie toutes les commandes.

**Terminal 1 : Déploiement**
```bash
make deploy
```

Ce qui va se passer :
- Vérification et démarrage de Minikube si nécessaire
- Déploiement du namespace `japaninside`
- Déploiement de PostgreSQL (attente qu'il soit prêt)
- Déploiement du backend (3 replicas)
- Déploiement du frontend (3 replicas)
- Attente que tous les pods soient prêts

**Terminal 2 : Tunnel LoadBalancer** (dans un nouveau terminal)
```bash
make tunnel
```

- Ce terminal doit rester ouvert pendant toute la session !
- Vous aurez besoin de `sudo`

**Vérifier le statut** (retour au Terminal 1)
```bash
make status
```

Affiche les pods, services, et URLs d'accès !

#### Commandes disponibles

| Commande | Description |
|----------|-------------|
| `make deploy` | Déploie l'application complète avec LoadBalancer |
| `make tunnel` | Lance le tunnel Minikube (requis, garder ouvert) |
| `make status` | Affiche l'état des pods et les URLs d'accès |
| `make logs-backend` | Logs en temps réel du backend |
| `make logs-frontend` | Logs en temps réel du frontend |
| `make logs-all` | Logs de tous les services |
| `make endpoints` | Affiche les endpoints (distribution du trafic) |
| `make scale-up` | Scale à 5 replicas (backend + frontend) |
| `make scale-down` | Scale à 2 replicas |
| `make clean` | Supprime tous les déploiements |
| `make redeploy` | Nettoie et redéploie |
| `make help` | Affiche toutes les commandes disponibles |

#### Workflow complet

```bash
# Terminal 1
make deploy
make status

# Terminal 2 (nouveau terminal, laisser ouvert)
make tunnel

# Terminal 1 (après quelques secondes)
make status  # Voir les URLs avec IPs externes

# Ouvrir dans le navigateur l'URL affichée !

# Voir les logs en temps réel
make logs-backend

# Scaler selon les besoins
make scale-up      # Plus de capacité
make scale-down    # Économiser les ressources

# Nettoyage
make clean
```

---

### 🪟 Windows

#### Prérequis

- **Minikube**
- **kubectl** 
- **PowerShell**

#### Démarrage rapide avec PowerShell

**Terminal 1 : Déploiement** (PowerShell en Administrateur)

```powershell
.\scripts\deploy.ps1
```

Ce qui va se passer :
- Vérification et démarrage de Minikube si nécessaire
- Déploiement du namespace `japaninside`
- Déploiement de PostgreSQL (attente qu'il soit prêt)
- Déploiement du backend (3 replicas)
- Déploiement du frontend (3 replicas)
- Attente que tous les pods soient prêts

**Terminal 2 : Tunnel LoadBalancer** (nouveau PowerShell en Administrateur)

```powershell
.\scripts\tunnel.ps1
```

- Ce terminal doit rester ouvert pendant toute la session !
- Nécessite les privilèges Administrateur

**Vérifier le statut** (retour au Terminal 1)

```powershell
.\scripts\status.ps1
```

Affiche les pods, services, et URLs d'accès.

#### Scripts disponibles

| Script | Description |
|--------|-------------|
| `.\scripts\deploy.ps1` | Déploie l'application complète |
| `.\scripts\tunnel.ps1` | Lance le tunnel (requis, garder ouvert) |
| `.\scripts\status.ps1` | Affiche l'état et les URLs |
| `.\scripts\logs.ps1` | Logs backend (par défaut) |
| `.\scripts\logs.ps1 frontend` | Logs frontend |
| `.\scripts\logs.ps1 all` | Logs de tous les services |
| `.\scripts\clean.ps1` | Supprime tous les déploiements |

#### Scaling manuel (Windows)

```powershell
# Augmenter à 5 replicas
kubectl scale deployment backend -n japaninside --replicas=5
kubectl scale deployment frontend -n japaninside --replicas=5

# Réduire à 2 replicas
kubectl scale deployment backend -n japaninside --replicas=2
kubectl scale deployment frontend -n japaninside --replicas=2

# Vérifier
kubectl get pods -n japaninside
```

#### Workflow complet

```powershell
# Terminal 1 (PowerShell Administrateur)
.\scripts\deploy.ps1
.\scripts\status.ps1

# Terminal 2 (nouveau PowerShell Administrateur, laisser ouvert)
.\scripts\tunnel.ps1

# Terminal 1 (après quelques secondes)
.\scripts\status.ps1  # Voir les URLs avec IPs externes

# Ouvrir dans le navigateur l'URL affichée !

# Voir les logs
.\scripts\logs.ps1

# Nettoyage
.\scripts\clean.ps1
```


Ouvrir PowerShell avec "Exécuter en tant qu'administrateur"

---

### Configuration LoadBalancer

Les services utilisent le type `LoadBalancer` pour distribuer automatiquement le trafic entre les replicas.

**Fichier : `k8s/backend/service.yaml`**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend
  namespace: japaninside
spec:
  type: LoadBalancer
  selector:
    app: backend
  ports:
    - protocol: TCP
      port: 8000
      targetPort: 8000
```