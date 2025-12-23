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
| Déploiement | Minikube |

---

## Structure du projet

```
.
├── backend
│   ├── __pycache__
│   ├── crud
│   ├── data
│   ├── models
│   ├── routes
│   ├── schemas
│   ├── tests
│   └── utils
├── frontend
│   ├── node_modules
│   ├── public
│   └── src
└── k8s
    ├── backend
    ├── config
    ├── db
    └── frontend
```

Le projet inclut des **tests unitaires** pour le front et le back, des **Makefiles**, des **pre-commit hooks**, et un code prêt pour la production.

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

Lors d’un push sur la branche \`main\` :

1. Build des images Docker (Dockerfile.prod front et back)  
2. Déploiement des images sur Docker Hub  
3. Récupération des images depuis Docker Hub vers Minikube  
4. Lancement de l’application localement sur Minikube (simule un environnement Kubernetes de production)
